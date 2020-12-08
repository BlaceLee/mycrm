from sales import models


def qq(par):
    return models.Customers.objects.filter(qq__startswith=par)


def qq_name(par):
    return models.Customers.objects.filter(qq_name__startswith=par)


def name(par):
    return models.Customers.objects.filter(name__startswith=par)


def status(par):
    return models.Customers.objects.filter(status__startswith=par)


def data(par):
    return models.Customers.objects.filter(date=par)


course_type = {'Linux': 'Linux中高级', 'PythonFullStack': 'Python高级全栈开发'},


def course(par):
    print('par', par)
    print(models.Customers.objects.filter(course='Linux'))
    return models.Customers.objects.filter(course='Linux中高级')