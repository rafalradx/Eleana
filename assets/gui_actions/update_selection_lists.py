class Update():

    def dataset_list(self, dataset: list) -> list:
        # This function is used to create list of data for all
        names = ['None']
        i = 0
        for data in dataset:
            name = str(i + 1) + '. ' + data.name
            names.append(name)
            i += 1

        return names

    def data_in_group_list(self, dataset: list, eleana_selections: dict, assignmentToGroups: dict):
        # This function is used to create list of data that belongs to the group which is currently selected
        group = eleana_selections['group']
        data_list = assignmentToGroups[group]
        names = ['None']
        for index in data_list:
            name = str(index+1) + '. ' + dataset[index]
            names.append(name)
        return names



    def results_list(self, results):
        names = []
        i = 1
        for data in dataset:
            name = data.name
            name = str(i) + ". " + name
            names.append(name)
            i += 1
        return names

        #     for name in names:
        #         name = str(i) + '. ' + name
        #         names = names + name
        #     #name.append(data.name)
        # print(names)


    # Creating groups on basis of groups defined in Eleana.dataset
    def groups(self, dataset):
        found_groups = set()
        self.groups = []
        for data in dataset:
            self.groups.extend(data.groups)
        found_groups.update(self.groups)

        self.assignToGroups ={}
        for group_name in found_groups:

            i = 0
            spectra_numbers = []
            while i < len(dataset):
                groups_in_single_spectrum = dataset[i].groups
                if group_name in groups_in_single_spectrum:
                    spectra_numbers.append(i)
                i += 1
            self.assignToGroups[group_name] = spectra_numbers
        return self.assignToGroups


    def firstComobox(self, selections: dict, groups: dict):


        pass
