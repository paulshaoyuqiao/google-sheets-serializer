def create_filter(reader):
    return Filter(reader)


class Filter:
    def __init__(self, reader):
        from gserializer.Tools.Reader import Reader
        if type(reader) is not Reader:
            print("Value Error: cannot properly read data from the given link")
            print("Please make sure you have the right access right and the correct sheetID")
        self.data = reader.values

    def get_transpose(self):
        data_copy = list(self.data)
        if self.__col__() != self.__row__():
            return data_copy
        for i in range(len(self.data)):
            for j in range(len(self.data[0])):
                data_copy[i][j] = self.data[j][i]
        return data_copy

    def __len__(self):
        return len(self.data)

    def __col__(self):
        return len(self.data[0])

    def __row__(self):
        return self.__len__()

    def num_cols(self):
        return self.__col__()

    def num_rows(self):
        return self.__row__()

    def int_values(self):
        return self.map(lambda x: int(x))

    def float_values(self):
        return self.map(lambda x: float(x))

    def colnames(self):
        return self.data[0]

    def values(self):
        return self.data[1:]

    def print_grid(self, grid):
        cols = range(self.num_cols())
        widths = [max([len(str(row[c])) for row in grid]) for c in cols]
        for row in grid:
            line = ''
            for col in cols:
                element = str(row[col])
                line = line + element + ' ' * (widths[col] - len(element) + 1)
            print(line)

    def print_formatted(self):
        placeholders = ["%s"] * self.num_cols()
        placeholders = " ".join(placeholders)
        column_header = ("Columns: " + placeholders) % tuple(self.colnames())
        print(column_header)
        self.print_grid(self.values())

    def map(self, func):
        mapped_data = []
        col_names = self.colnames()
        mapped_data.append(col_names)
        for data_row in self.data[1:]:
            mapped_data.append([func(x) for x in data_row])
        return mapped_data

    @staticmethod
    def filter_reduce(L, func):
        return [x for x in L if func(x)]

    @staticmethod
    def filter_reduce_by_index(L, func):
        return [L[i] for i in range(len(L)) if func(i)]

    def filter(self, major_order=0, func=lambda x: True, numerical=0):
        if numerical == 1: # integer
            values = self.int_values()
        elif numerical == 2: # floats
            values = self.float_values()
        else: # remain unchanged
            values = self.values()
        filtered_data = []
        col_names = self.colnames()
        if major_order == 0:  # Row major order
            filtered_data.append(col_names)
            for data_row in values:
                if all(list(map(func, data_row))):
                    filtered_data.append(data_row)
        elif major_order == 1:  # Column major order
            valid_columns = []
            for col_index in range(len(col_names)):
                column = [values[row_index][col_index] for row_index in range(1, self.__row__())]
                if all(map(func, column)):
                    filtered_data.append(column)
                    valid_columns.append(col_index)
            filtered_data = [Filter.filter_reduce_by_index(col_names, lambda x: x in valid_columns)] + filtered_data
        else:
            return ValueError("The major order can only 0 (row-major) or 1 (column-major)")
        return filtered_data

    @staticmethod
    def accumulate_reduce(L, func):
        if len(L) <= 1:
            return L
        else:
            L[1] = func(L[0], L[1])
            return Filter.accumulate_reduce(L[1:], func)

    def reduce(self, major_order=0, func=None, numerical=0):
        if numerical == 1: # integer
            values = self.int_values()
        elif numerical == 2: # floats
            values = self.float_values()
        else: # remain unchanged
            values = self.values()
        if func is None:
            return self.data
        reduced_data = []
        col_names = self.colnames()
        if major_order == 0:  # Row major order
            for data_row in values:
                reduced_data.append(Filter.accumulate_reduce(data_row, func))
        elif major_order == 1:  # Col major order
            reduced_data.append(col_names)
            reduced_row = []
            for col_index in range(len(col_names)):
                column = [values[row_index][col_index] for row_index in range(1, self.__row__())]
                reduced_column = Filter.accumulate_reduce(column, func)
                reduced_row.extend(reduced_column)
            reduced_data.append(reduced_row)
        else:
            return ValueError("The major order can only 0 (row-major) or 1 (column-major)")
        return reduced_data
