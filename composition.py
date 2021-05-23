# Composition models "has a relationship" - It enables creating complex types by combing objects of other types

# In composition, a class known as composite contains an object of another class known as component
# In other words, a composite class has a component of another class.

# Composition allows composite classes to reuse the implementation of the components it contains.
# The composite class doesn’t inherit the component class interface, but it can leverage its implementation.
# The composition relation between two classes is considered loosely coupled.

# An employee HAS AN id and a name (its COMPOSED of an id and name).
# We can also say, they have an address.

class Employee:
    def __init__(self, id_, name):
        self.id = id_
        self.name = name
        self.address = None

    def work(self):
        return f'{self.name} is working'

    def calculate_payroll(self):
        pass


class Address:
    def __init__(self, city, street):
        self.city = city
        self.street = street

    def __str__(self):
        return f'City: {self.city} Street: {self.street}'


my_address = Address('Hamilton', '409 Upper wentworth st')


# Now that we've defined an address class, we can now add it to the employee class through composition
# We initialize address to None for now to make it an optional param, by doing that we can now assign address to an employee.
# This is a loosely coupled relationship.
# The employee class leverages the implementation of the Address class without any knowledge of what an Address object is or represented.
# This type of design is so flexible that you cn the Address class without any impact to the Employee class.

class ManagerRole:
    @staticmethod
    def perform_duties(hours):
        return f'screams and yells for {hours} hours'


class SalesRole:
    @staticmethod
    def perform_duties(hours):
        return f'does paperwork for {hours} hours'


# This is a flexible design, the system is composed of different roles. We can now implement as many role classes as we want
# The role classes are independent of each other, but they expose the same interface, so they are interchangeable.
class ProductivitySystem:
    def __init__(self):
        self._roles = {
            'manager': ManagerRole,
            'sales': SalesRole
        }

    def get_role(self, role_id):
        role_type = self._roles.get(role_id)
        if not role_type:
            raise ValueError('role_id')
        return role_type()

    def track(self, employees, hours):
        for employee in employees:
            employee.work(hours)


class PayrollPolicy:
    def __init__(self):
        self.hours_worked = 0

    def track_work(self, hours):
        self.hours_worked += hours


class SalaryPolicy(PayrollPolicy):
    def __init__(self, weekly_salary):
        super().__init__()
        self.weekly_salary = weekly_salary

    def calculate_payroll(self):
        return self.weekly_salary


class HourlyPolicy(PayrollPolicy):
    def __init__(self, hour_rate):
        super().__init__()
        self.hour_rate = hour_rate

    def calculate_payroll(self):
        return self.hours_worked * self.hour_rate


class PayrollSystem:
    def __init__(self):
        self._employee_policies = {
            1: SalaryPolicy(3000),
            2: HourlyPolicy(9)
        }

    def get_policy(self, employee_id):
        policy = self._employee_policies.get(employee_id)
        if not policy:
            return ValueError(employee_id)
        return policy

    def calculate_payroll(self, employees):
        print('Calculating Payroll')
        print('===================')
        for employee in employees:
            print(f'Payroll for: {employee.id} - {employee.name}')
            print(f'- Check amount: {employee.calculate_payroll()}')
            if employee.address:
                print('- Sent to:')
                print(employee.address)
            print('')


# The PayrollSystem keeps an internal database of payroll policies for each employee.
# It exposes a .get_policy() that, given an employee id, returns its payroll policy.
# If a specified id doesn’t exist in the system, then the method raises a ValueError exception.

class AddressBook:
    def __init__(self):
        self._employee_addresses = {
            1: Address('121 Admin Rd.', 'Concord', 'NH', '03301'),
            2: Address('67 Paperwork Ave', 'Manchester', 'NH', '03101'),
            3: Address('15 Rose St', 'Concord', 'NH', '03301', 'Apt. B-1'),
            4: Address('39 Sole St.', 'Concord', 'NH', '03301'),
            5: Address('99 Mountain Rd.', 'Concord', 'NH', '03301'),
        }

    def get_employee_address(self, employee_id):
        address = self._employee_addresses.get(employee_id)
        if not address:
            raise ValueError(employee_id)
        return address


# The employee database keeps track of all employees in the company. It is composed of a productivity system,
# pay roll system and employee address book.

class EmployeeDatabase:
    def __init__(self):
        self._employees = [
            {
                'id': 1,
                'name': 'Mary Poppins',
                'role': 'manager'
            },
            {
                'id': 2,
                'name': 'John Smith',
                'role': 'secretary'
            }
        ]
        self.productivity = ProductivitySystem()
        self.payroll = PayrollSystem()
        self.employee_addresses = AddressBook()

    @property
    def employees(self):
        return [self._create_employee(**data) for data in self._employees]

    def _create_employee(self, id, name, role):
        address = self.employee_addresses.get_employee_address(id)
        employee_role = self.productivity.get_role(role)
        payroll_policy = self.payroll.get_policy(id)
        return Employee(id, name, address, employee_role, payroll_policy)