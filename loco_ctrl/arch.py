'''
Archiving functions for LocoCtrl
'''
import os
import os.path
import csv

def create_arch(self, arch_path):
    '''
    Create the archives for LocoCtrl.

    Will create a subdir in the `arch_path` directory named 'LocoCtrl' and
    create the following archive CSV files:
    * TODO
    '''

    # Check that arch_path is a valid directory
    if not os.path.isdir(arch_path):
        print(f'Cannot create LocoCtrl archives as {arch_path} is not a valid'
              ' directory')
        raise NotADirectoryError()

    # Create the module directory
    mod_dir = os.path.join(arch_path, 'LocoCtrl')
    os.mkdir(mod_dir)

    # List of tuples storing filenames and parameter names for each file. The
    # parameter names must be available to the LocoCtrl instance.
    arch_files = [
        ('LocoCtrl_mnvr_cmd', [
            'mnvr_cmd.mnvr_id',
            'mnvr_cmd.mnvr_params["rov_speed_mss_Lm"]',
            'mnvr_cmd.mnvr_params["curv_m_Rb"]',
            'mnvr_cmd.mnvr_params["rov_rate_rads_Rb"]'])
    ]

    # Create the CSV writer objects
    self.arch_writers = {}

    # For all the files to write
    for arch_file in arch_files:
        # File name
        file_name = os.path.join(mod_dir, f'{arch_file[0]}.csv')

        # Open the file
        csvfile = open(file_name, 'w+')

        # Add the elapsed time to the fieldnames
        arch_file[1].insert(0, 'ret_s')

        # Create the dict writer and save the fieldnames for this file
        self.arch_writers[arch_file[0]] = (
            csvfile,
            csv.DictWriter(csvfile, fieldnames=arch_file[1], extrasaction='ignore'),
            arch_file[1]
        )

        # Write the header line out
        self.arch_writers[arch_file[0]][1].writeheader()

def write_arch(self, ret_s):
    '''
    Write the archive CSVs for this simulation time
    '''

    # Make a copy of the module's dict so we can set any missing parameter to
    # zero.
    mod_dict = self.__dict__.copy()

    # Set the simulation time
    mod_dict['ret_s'] = f'{ret_s:.2f}'

    # Iterate over the archive writers
    for mod_name, arch_writer in self.arch_writers.items():

        # If one of the fields is missing attempt to get it, otherwise set to
        # zero
        for field in arch_writer[2]:
            if field not in mod_dict.keys():
                # Use of eval is a security risk but none of it should be coming
                # form external sources so it's ok (maybe)
                field_escaped = field.replace('"', "'")
                mod_dict[field] = eval(f'self.__dict__.get("{field_escaped}")')

        # Write the data
        arch_writer[1].writerow(mod_dict)

def close_arch(self):
    '''
    Close the open archive file
    '''

    for mod_name, arch_writer in self.arch_writers.items():
        arch_writer[0].close()
