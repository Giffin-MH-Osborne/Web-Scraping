class Job:
    title: str
    company: str
    location: str
    salary: str
    link: str

    def __init__(self, title, company, location, salary, link):
        self.title = title
        self.company = company
        self.location = location
        self.salary = salary
        self.link = link

    def csv_format(self):
        salary = self.salary.replace(',','')
        csv_string = self.title + ', ' + self.company + ', ' + self.location + ', ' + salary + ', ' + self.link + '\n'

        return csv_string

    def display(self):
        print("Title: {0}".format(self.title))
        print("Company: {0}".format(self.company))
        print("Location: {0}".format(self.location))
        print("Salary: {0}".format(self.salary))
        print("Link: {0}".format(self.link))
        print('-'*20 + '\n')

