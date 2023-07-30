import logging
import json
from requests import request, HTTPError
from urllib.parse import urlparse, urlencode
from typing import Union
from .constants import BASE_URL, API_PATH
from .exceptions import ClientException
from .models import (
    Report,
    User,
    Account,
    Contact,
    Project,
    Task,
    TimeEntry,
    Dock
)

logger = logging.getLogger("MinuteDock")


class MinuteDockCall(object):
    def __init__(self, api_key: str, account_id: str = None):

        self.api_key = api_key
        self.account_id = account_id

        # Check if account_id was specified.
        if (account_id is None):
            # Only set api key in header.
            self.headers = {"X-API-Key": api_key}
        else:
            # set both api key and account_id in header.
            self.headers = {
                "X-API-Key": api_key,
                "X-Account-ID": account_id
            }

    def __repr__(self) -> str:
        return "MinuteDock('{0}', '{1}')".format(self.api_key, self.account_id)

    def _make_request(self, method: str, path: str, payload: dict = None) -> dict:
        """
        The function `_make_request` sends an HTTP request with the specified method, path, and payload,
        and returns the JSON response.
        
        Args:
          method (str): The `method` parameter is a string that specifies the HTTP method to be used for
        the request, such as "GET", "POST", "PUT", "DELETE", etc.
          path (str): The `path` parameter is a string that represents the URL path for the request. It
        specifies the endpoint or resource that the request is being made to.
          payload (dict): The `payload` parameter is a dictionary that contains the data to be sent in
        the request body. It is optional and is set to `None` if no payload is required for the
        request.
        
        Returns:
          a dictionary, which is the JSON response from the request.
        """
        request_headers = self.headers
        request_payload = payload

        if payload is not None:
            # remove none key-value pairs first.
            request_payload = self.__remove_none_values(payload)
            # set content-type in header.
            request_headers["Content-Type"] = "application/json"

        try:
            # Make request with given info
            md_response = request(
                method=method,
                url=path,
                headers=request_headers,
                data=request_payload
            )

            # raise error if status is HTTPError
            md_response.raise_for_status()
        except HTTPError as e:
            # Exit with the specified http error code.
            raise SystemExit(e)
        else:
            # If no error, return json response.
            return md_response.json()

    def _get(self, cls, **kwargs) -> Union[object, list[object]]:
        """
        The function `_get` retrieves either a single MinuteDock object or a list of MinuteDock objects 
        based on the specified parameters.

        Args:
          cls: The `cls` parameter is a reference to the MinuteDock object.

        Returns:
            a single MinuteDock object or a list of MinuteDock objects.
        """
        path = kwargs.get("path", None)
        path_var = kwargs.get("path_var", None)
        params = kwargs.get("params", None)

        api_url = self.__api_url(path=path, path_var=path_var, params=params)
        md_response = self._make_request(method="GET", path=api_url)

        return self._handle_response(cls, md_response)

    def _post(self, cls, **kwargs) -> object:
        """
        The function `_post` creates a single MinuteDock object based on the specified parameters.

        Args:
          cls: The `cls` parameter is a reference to the MinuteDock object.

        Returns:
            a single MinuteDock object.
        """
        path = kwargs.get("path", None)
        path_var = kwargs.get("path_var", None)
        payload = kwargs.get("payload", None)

        api_url = self.__api_url(path, path_var)
        md_response = self._make_request(
            method="POST",
            path=api_url,
            payload=payload
        )

        return self._handle_response(cls, md_response)

    def _put(self, cls, **kwargs) -> object:
        """
        The function `_put` updates a single MinuteDock object based on the specified parameters.

        Args:
          cls: The `cls` parameter is a reference to the MinuteDock object.

        Returns:
            a single MinuteDock object.
        """
        path = kwargs.get("path", None)
        id = kwargs.get("id", None)
        payload = kwargs.get("payload", None)

        api_url = self.__api_url(path, id)
        md_response = self._make_request(
            method="PUT",
            path=api_url,
            payload=payload
        )

        return self._handle_response(cls, md_response)

    def _handle_response(self, cls, response: str) -> Union[object, list[object]]:
        """
        The `_handle_response` function takes a response string and a class, and returns an object or a
        list of objects created from the response.

        Args:
          cls: The parameter `cls` is a class object. It is used to create an instance of the class and
        populate its attributes based on the provided response.
          response (str): The `response` parameter is the json encoded response from the api request.

        Returns:
          an object or a list of objects.
        """
        return cls._create_from_dict(response)

    def __api_url(self, path: str, path_var: str = None, params: dict = None) -> str:
        if (path is not None):
            url_parts = urlparse(BASE_URL)

            if (params is not None):
                query = urlencode(params)
                url_parts = url_parts._replace(query=query)

            if (path_var is not None):
                path += f"/{path_var}"

            url_parts = url_parts._replace(path=path)

            return url_parts.geturl().lower()
        else:
            raise ClientException("path must not be None.")

    def __remove_none_values(self, data: dict) -> str:
        """
        The `_remove_none_values` function removes any key-value pairs with a value of None 
        from a given dictionary and returns the resulting dictionary as a JSON string.

        Args:
            data (dict): The `data` parameter is a dictionary that contains key-value pairs.

        Returns:
            A JSON formatted string of the dictionary `_data` after removing any key-value 
            pairs where the value is `None`.
        """
        # Copy data to a new variable.
        _data = data.copy()

        # Iterate over the key-value pairs in data.
        for key, value in data.items():
            # remove a key-value pair if value is None.
            if value is None:
                _data.pop(key)

        # Return a json formatted string
        return json.dumps(_data)


class MinuteDock(MinuteDockCall):
    """
    The MinuteDock class is a subclass of the MinuteDockCall class.

    Please refer to the MinuteDock API documentation for more information on each function.
    https://developer.minutedock.com
    """

    def __init__(self, api_key: str, account_id: str = None):
        """
        This function initializes a MinuteDock API object with an API key and an optional account ID.

        Args:
            api_key (str): The `api_key` parameter is a string that represents the API key used to
                authenticate and authorize access to the MinuteDock API. This key is provided by the
                MinuteDock service and can be found within your MinuteDock profile.
            account_id (str): The `account_id` parameter is an optional parameter that represents the
                unique identifier for a MinuteDock account. If provided, it allows the API object to make
                requests to a specific account. If not provided, the API object will make requests to the 
                current authenticated account.
        """
        MinuteDockCall.__init__(self, api_key, account_id)

    def get_report(
        self,
        users: Union[list[int], str] = "all",
        contacts: Union[list[int], str] = "all",
        projects: Union[list[int], str] = "all",
        tasks: Union[list[int], str] = "all",
        billable_only: bool = False,
        unbillable_only: bool = False,
        invoiced_only: bool = False,
        uninvoiced_only: bool = False,
        date_from: str = None,
        date_to: str = None,
        task_detail: str = "",
    ) -> Report:
        """
        The `get_report` function retrieves a MinuteDock report based on the provided parameters.

        Returns:
            a `Report` object.
        """
        return self._post(
            cls=Report,
            path=API_PATH["reports"],
            params={
                "users":            users,
                "contacts":         contacts,
                "projects":         projects,
                "tasks":            tasks,
                "billable_only":    billable_only,
                "unbillable_only":  unbillable_only,
                "invoiced_only":    invoiced_only,
                "uninvoiced_only":  uninvoiced_only,
                "from":             date_from,
                "to":               date_to,
                "task_detail":      task_detail,
            }
        )

    def get_all_users(self, active: bool = False) -> list[User]:
        """
        The `get_all_users` function lists all Users in the account.

        Returns:
            a list of User objects.
        """
        return self._get(cls=User, path=API_PATH["users"], params={"active": active})

    def get_current_user(self) -> User:
        """
        The `get_current_user` function gets information about the current authenticated user.

        Returns:
            a User object.
        """
        return self._get(cls=User, path=API_PATH["current_user"])

    def get_accounts(self) -> list[Account]:
        """
        The `get_accounts` function returns a list of all Accounts available to the user.

        Returns:
            A list of Account objects.
        """
        return self._get(cls=Account, path=API_PATH["accounts"])

    def get_current_account(self) -> Account:
        """
        The `get_current_account` function gets information about the current authenticated account.

        Returns:
            an Account object.
        """
        return self._get(cls=Account, path=API_PATH["current_account"])

    def get_contact(self, id: int) -> Contact:
        """
        The `get_contact` function retrieves a single contact from MinuteDock.

        Returns:
            a contact object
        """
        return self._get(cls=Contact, path_var=id, path=API_PATH["contacts"])

    def get_all_contacts(self, pinned: bool = False, active: bool = True) -> Contact:
        """
        The `get_all_contacts` function retrieves all contacts from MinuteDock.

        Returns:
            a contact object
        """
        return self._get(
            cls=Contact,
            path=API_PATH["contacts"],
            params={
                "pinned": pinned,
                "active": active
            }
        )

    def create_contact(
        self,
        id: int = None,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        short_code: str = None,
        active: bool = None,
    ) -> Contact:
        """
        The `create_contact` function creates a new contact with the specified parameters.

        Returns:
            a contact object.
        """
        return self._post(
            cls=Contact,
            path=API_PATH["contacts"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "short_code":           short_code,
                "active":               active
            }
        )

    def update_contact(
        self,
        id: int,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        short_code: str = None,
        active: bool = None,
    ) -> Contact:
        """
        The `update_contact` function updates an existing MinuteDock contact.

        Returns:
            a contact object with updated attributes.
        """
        return self._put(
            cls=Contact,
            path_var=id,
            path=API_PATH["contacts"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "short_code":           short_code,
                "active":               active
            }
        )

    def get_project(self, id: int) -> Project:
        """
        The `get_project` function retrieves a single project from MinuteDock.

        Returns:
            a project object
        """
        return self._get(cls=Project, path_var=id, path=API_PATH["projects"])

    def get_all_projects(self, pinned: bool = False, active: bool = True) -> Project:
        """
        The `get_all_projects` function retrieves all projects from MinuteDock.

        Returns:
            a project object
        """
        return self._get(
            cls=Project,
            path=API_PATH["projects"],
            params={
                "pinned": pinned,
                "active": active
            }
        )

    def create_project(
        self,
        id: int = None,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        contact_id: int = None,
        short_code: str = None,
        active: bool = True,
        hidden: bool = False,
        description: str = None
    ) -> Project:
        """
        The `create_project` function creates a new project with the specified parameters.

        Returns:
            a project object.
        """
        return self._post(
            cls=Project,
            path=API_PATH["projects"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "contact_id":           contact_id,
                "short_code":           short_code,
                "active":               active,
                "hidden":               hidden,
                "description":          description
            }
        )

    def update_project(
        self,
        id: int,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        contact_id: int = None,
        short_code: str = None,
        active: bool = None,
        hidden: bool = None,
        description: str = None
    ) -> Project:
        """
        The `update_project` function updates an existing MinuteDock project.

        Returns:
            a project object with updated attributes.
        """
        return self._put(
            cls=Project,
            path_var=id,
            path=API_PATH["projects"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "contact_id":           contact_id,
                "short_code":           short_code,
                "active":               active,
                "hidden":               hidden,
                "description":          description
            }
        )

    def get_task(self, id: int) -> Task:
        """
        The `get_task` function retrieves a single task from MinuteDock.

        Returns:
            a Task object 
        """
        return self._get(cls=Task, id=id, path=API_PATH["tasks"])

    def get_all_tasks(self, pinned: bool = None, active: bool = True) -> list[Task]:
        """
        The `get_all_tasks` function retrieves all tasks from MinuteDock.

        Returns:
            a list of Task objects
        """
        return self._get(
            cls=Task,
            path=API_PATH["tasks"],
            params={
                "pinned": pinned,
                "active": active
            }
        )

    def create_task(
        self,
        id: int = None,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        contact_id: int = None,
        short_code: str = None,
        active: bool = None,
        hidden: bool = None,
        description: str = None
    ) -> Task:
        """
        The `create_task` function creates a new task with the specified parameters.

        Returns:
            a task object.
        """
        return self._post(
            cls=Task,
            path=API_PATH["tasks"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "contact_id":           contact_id,
                "short_code":           short_code,
                "active":               active,
                "hidden":               hidden,
                "description":          description
            }
        )

    def update_task(
        self,
        id: int,
        budget_type: str = None,
        budget_frequency: str = None,
        budget_target: float = None,
        budget_progress: float = None,
        default_rate_dollars: str = None,
        pinned: bool = None,
        name: str = None,
        contact_id: int = None,
        short_code: str = None,
        active: bool = None,
        hidden: bool = None,
        description: str = None
    ) -> Task:
        """
        The `update_task` function updates an existing MinuteDock task.

        Returns:
            a task object with updated attributes.
        """
        return self._put(
            cls=Task,
            path_var=id,
            path=API_PATH["tasks"],
            params={
                "id":                   id,
                "budget_type":          budget_type,
                "budget_frequency":     budget_frequency,
                "budget_target":        budget_target,
                "budget_progress":      budget_progress,
                "default_rate_dollars": default_rate_dollars,
                "pinned":               pinned,
                "name":                 name,
                "contact_id":           contact_id,
                "short_code":           short_code,
                "active":               active,
                "hidden":               hidden,
                "description":          description
            }
        )

    def start_timer(self) -> TimeEntry:
        """
        The `start_timer` function starts a timer for a time entry.

        Returns:
          a `TimeEntry` object.
        """
        return self._post(cls=TimeEntry, path_var="start", path=API_PATH["current_entry"])

    def pause_timer(self) -> TimeEntry:
        """
        The `pause_timer` function pauses a timer for a time entry.

        Returns:
          a `TimeEntry` object.
        """
        return self._post(cls=TimeEntry, path_var="pause", path=API_PATH["current_entry"])

    def log_timer(self) -> TimeEntry:
        """
        The `log_timer` function logs a timer for a time entry.

        Returns:
          a `TimeEntry` object.
        """
        return self._post(cls=TimeEntry, path_var="log", path=API_PATH["current_entry"])

    def search_time_entries(
        self,
        date_from: str = None,
        date_to: str = None,
        limit: int = 50,
        offset: int = 0,
        users: Union[list[int], str] = "all",
        contacts: Union[list[int], str] = "all",
        projects: Union[list[int], str] = "all",
        tasks: Union[list[int], str] = "all",
        billable_only: bool = False,
        unbillable_only: bool = False,
        invoiced_only: bool = False,
        uninvoiced_only: bool = False,
        since: str = None
    ) -> Union[list[TimeEntry], TimeEntry]:
        """
        The `search_time_entries` function searches for and returns the time entries 
        that match the input parameters. Only returns the first 50 by default. Use
        Offset to page results.

        Returns:
          a list of `TimeEntry` objects.
        """
        return self._get(
            cls=TimeEntry,
            path=API_PATH["entries"],
            params={
                "from":             date_from,
                "to":               date_to,
                "limit":            limit,
                "offset":           offset,
                "users":            users,
                "contacts":         contacts,
                "projects":         projects,
                "tasks":            tasks,
                "billable_only":    billable_only,
                "unbillable_only":  unbillable_only,
                "invoiced_only":    invoiced_only,
                "uninvoiced_only":  uninvoiced_only,
                "since":            since
            }
        )

    def create_time_entry(
        self,
        id: int = None,
        account_id: int = None,
        description: str = None,
        duration: int = None,
        contact_id: int = None,
        project_id: int = None,
        task_ids: list[int] = None,
        invoice_id: int = None,
        logged_at: str = None,
    ) -> TimeEntry:
        """
        The `create_time_entry` function creates a new time entry with the specified parameters.
        
        Returns:
          a TimeEntry object.
        """
        return self._post(
            cls=TimeEntry,
            path=API_PATH["entries"],
            payload={
                "id":           id,
                "account_id":   account_id,
                "description":  description,
                "duration":     duration,
                "contact_id":   contact_id,
                "project_id":   project_id,
                "task_ids":     task_ids,
                "invoice_id":   invoice_id,
                "logged_at":    logged_at
            }
        )

    def update_time_entry(
        self,
        id: int,
        account_id: int = None,
        description: str = None,
        duration: int = None,
        contact_id: int = None,
        project_id: int = None,
        task_ids: list[int] = None,
        invoice_id: int = None,
        logged_at: str = None,
    ) -> TimeEntry:
        """
        The `update_time_entry` function updates an existing time entry with the specified parameters.
        
        Returns:
          a TimeEntry object.
        """
        return self._put(
            cls=TimeEntry,
            path_var=id,
            path=API_PATH["entries"],
            payload={
                "id":           id,
                "account_id":   account_id,
                "description":  description,
                "duration":     duration,
                "contact_id":   contact_id,
                "project_id":   project_id,
                "task_ids":     task_ids,
                "invoice_id":   invoice_id,
                "logged_at":    logged_at
            }
        )


__all__ = ["MinuteDock"]
