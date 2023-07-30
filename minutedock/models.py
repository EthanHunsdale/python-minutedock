import json
from .exceptions import ClientException


class BaseModel(object):
    def __init__(self, **kwargs):
        """Base class that all MinuteDock models inherit from."""
        self.attribute_defaults = {}

    def __str__(self):
        """A string representation of BaseModel"""
        return self.to_json_string()

    def __eq__(self, _value: object) -> bool:
        return _value.to_dict() == self.to_dict()

    def __ne__(self, _value: object) -> bool:
        return not self.__eq__(_value)

    def __hash__(self) -> int:
        if hasattr(self, "id"):
            return hash(self.id)
        else:
            return hash(self.description, self.total_entries, self.total_hours)

    def __getattr__(self, _name: str):
        try:
            return object.__getattr__(self, _name)
        except AttributeError:
            raise ClientException(
                "The attribute does not exist in this object."
            )

    def to_json_string(self) -> str:
        return json.dumps(self.to_dict(), sort_keys=True)

    def to_dict(self) -> dict:
        data = dict()

        for key, value in self.attribute_defaults.items():
            if isinstance(getattr(self, key, None), (list, tuple, set)):
                data[key] = list()
                for obj in getattr(self, key, None):
                    if getattr(obj, "to_dict", None):
                        data[key].append(obj.to_dict())
                    else:
                        data[key].append(obj)
            elif getattr(getattr(self, key, None), "to_dict", None):
                data[key] = getattr(self, key).to_dict()
            elif getattr(self, key, None):
                data[key] = getattr(self, key, None)

        return data

    @classmethod
    def _create_from_dict(cls, _data: dict, **kwargs) -> object:
        if _data is None:
            return None

        json_data = _data.copy()

        if kwargs:
            for key, value in kwargs.items():
                json_data[key] = value

        if isinstance(json_data, list):
            obj_list = list()

            for value in json_data:
                class_obj = cls(**value)
                class_obj._json = _data
                obj_list.append(class_obj)

            return obj_list
        else:
            class_obj = cls(**json_data)
            class_obj._json = _data

            return class_obj


class Report(BaseModel):
    """A class representing a MinuteDock report"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "description":      None,
            "total_entries":    None,
            "hours":            None,
            "billable_hours":   None,
            "billable_value":   None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Report("{0}", "{1}", "{2}", "{3}", "{4}")'.format(
            self.description,
            self.total_entries,
            self.hours,
            self.billable_hours,
            self.billable_value,
        )


class User(BaseModel):
    """A class representing a MinuteDock User"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":           None,
            "email":        None,
            "first_name":   None,
            "last_name":    None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'User(ID="{0}", email="{1}", first_name="{2}", last_name="{3}")'.format(
            self.id,
            self.email,
            self.first_name,
            self.last_name
        )


class Account(BaseModel):
    """A class representing a MinuteDock Account"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":   None,
            "name": None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Account(ID="{0}", name="{1}")'.format(self.id, self.name)


class Contact(BaseModel):
    """A class representing a MinuteDock Contact"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":                   None,
            "budget_type":          None,
            "budget_frequency":     None,
            "budget_target":        None,
            "budget_progress":      None,
            "default_rate_dollars": None,
            "pinned":               None,
            "name":                 None,
            "short_code":           None,
            "active":               None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Contact(ID="{0}", active="{1}", name="{2}", short_code="{3}")'.format(
            self.id,
            self.active,
            self.name,
            self.short_code
        )


class Project(BaseModel):
    """A class representing a MinuteDock Project"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":                   None,
            "budget_type":          None,
            "budget_frequency":     None,
            "budget_target":        None,
            "budget_progress":      None,
            "default_rate_dollars": None,
            "pinned":               None,
            "name":                 None,
            "contact_id":           None,
            "short_code":           None,
            "active":               None,
            "hidden":               None,
            "description":          None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Project(ID="{0}", active="{1}", name="{2}", short_code="{3}")'.format(
            self.id,
            self.active,
            self.name,
            self.short_code
        )


class Task(BaseModel):
    """A class representing a MinuteDock Task"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":                   None,
            "budget_type":          None,
            "budget_frequency":     None,
            "budget_target":        None,
            "budget_progress":      None,
            "default_rate_dollars": None,
            "pinned":               None,
            "short_code":           None,
            "active":               None,
            "hidden":               None,
            "description":          None,
            "has_detail":           None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Task(ID="{0}", active="{1}", short_code="{2}")'.format(
            self.id,
            self.active,
            self.short_code
        )


class TimeEntry(BaseModel):
    """A class representing a MinuteDock Time Entry"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":           None,
            "account_id":   None,
            "description":  None,
            "duration":     None,
            "contact_id":   None,
            "project_id":   None,
            "task_ids":     None,
            "invoice_id":   None,
            "logged_at":    None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'TimeEntry(ID="{0}", logged_at="{1}" description="{2}", duration="{3}")'.format(
            self.id,
            self.logged_at,
            self.description,
            self.duration
        )


class Dock(BaseModel):
    """A class representing a MinuteDock Dock"""

    def __init__(self, **kwargs) -> None:
        self.attribute_defaults = {
            "id":           None,
            "account_id":   None,
            "description":  None,
            "duration":     None,
            "contact_id":   None,
            "project_id":   None,
            "task_ids":     None,
            "timer_active": None
        }

        for attribute, default in self.attribute_defaults.items():
            setattr(self, attribute, kwargs.get(attribute, default))

    def __repr__(self) -> str:
        return 'Dock(ID="{0}", description="{1}", duration="{2}", timer_active="{3}")'.format(
            self.id,
            self.description,
            self.duration,
            self.timer_active
        )
