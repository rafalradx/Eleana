class Update():

    def create_list_of_data(self, dataset: list):
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
