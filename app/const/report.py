import os


class Report:
    type: str
    description: str

    def __init__(self, _type, _description=''):
        self.type = _type
        self.description = _description

    def __repr__(self):
        return f"{self.__class__} at {hex(id(self))} with type: {self.type}"


class ReportCases:
    __slots__ = ['reports_dict', 'report_file', 'reports']

    def __init__(self, report_file):
        self.report_file = report_file
        self.reports_dict = {}
        self.reports = []
        for line in report_file.readlines():
            self.create_report_case_from_line(line)

    def create_report_case_from_line(self, line: str):
        if line == '':
            raise ValueError('parameter `line` cannot be an empty string')

        _n, _t, _d = (
            int(line.split('=')[0].split('.')[0]),
            line.split('=')[0].split('.')[1],
            line.split('=')[1]
        )
        report = Report(_type=_t, _description=_d)
        self.reports.append(report)

        _t = _t.replace(' ', '_')
        self[_t] = [_n, report]

    def create_report_case_from_values(self, _type, _description):
        n = len(self.reports)
        if _type.replace(' ', '_') in [r.type for r in self.reports]:
            raise NameError(
                'A case for the specified report already exists. Refer the {} file for more.'.format(
                    self.report_file.name.split("\\")[-1]
                ))
        report = Report(_type=_type, _description=_description)
        self.reports.append(report)
        _type = _type.replace(' ', '_')
        self[_type] = [n, report]

    def update_file(self):
        with open(self.report_file.name, 'w') as report_file:
            report_content = []
            for report in sorted(list(self.reports_dict.values()), key=lambda x: x[0]):
                report_content.append(''.join([
                    str(report[0]), '.', report[1].type, '=', report[1].description
                ]))
            report_file.write('\n'.join(report_content))

    def __repr__(self):
        return f'{self.__class__} at {hex(id(self))} with cases:{len(self.reports_dict.keys())}'

    def __len__(self):
        return len(self.reports_dict)

    def __setitem__(self, key, value):
        self.reports_dict[key] = value

    def __getitem__(self, item):
        if isinstance(item, int):
            return list(self.reports_dict.values())[item]
        return self.reports_dict[item]

    def __del__(self):
        self.report_file.close()
        del self


def set_new_report_case(ur_file, ur_type, ur_description):
    ur_report = ReportCases(ur_file)
    ur_report.create_report_case_from_values(_type=ur_type, _description=ur_description)
    ur_report.update_file()


REPORT_CONTENT_FILE = open(
    os.path.join(os.path.abspath('.'), 'report.content'),
    'r+'
)

REPORT_CONTENT_USER_FILE = open(
    os.path.join(os.path.abspath('.'), 'user_report.content'),
    'r+'
)

if __name__ == '__main__':
    cases = ReportCases(REPORT_CONTENT_FILE)
    print(cases)
    print('Default cases:')
    for i in cases.reports:
        print(i)

    print(cases[0])
    # set_new_report_case(REPORT_CONTENT_USER_FILE, 'Boom baamed', 'brightening flashes and ')
    set_new_report_case(REPORT_CONTENT_USER_FILE, 'Bamboozled',
                        'Being bamboozled by bamboozling bamboo pics :(')
