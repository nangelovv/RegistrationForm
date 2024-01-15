import unittest
from unittest.mock import patch
from services.users_services import *
from tests.tests_preparations import TestsPreparation

class ProfileTestCase(unittest.TestCase):
    def setUp(self):
        self.session = TestsPreparation().session
        self.session.query(Users).filter(Users.user_id != None).delete()
        self.session.commit()
        register(RegistrationData(email="newuser@example.com", first_name="New", last_name="User", password="password123"), self.session)
        self.user_id = try_login("newuser@example.com", "password123", self.session).user_id
        self.token = create_token(Users(user_id=self.user_id, email="newuser@example.com"))

    def test_try_login_returns_false_if_credentials_do_not_match(self):
        user = try_login("test@example.com", "wrongpassword", self.session)
        self.assertFalse(user)

    def test_try_login_returns_user_object_if_credentials_match(self):
        user = try_login("newuser@example.com", "password123", self.session)
        self.assertIsInstance(user, Users)

    def test_create_token_returns_string(self):
        user = Users(user_id="123", email="test@example.com")
        token = create_token(user)
        self.assertIsInstance(token, str)

    def test_verify_returns_accepted_response_if_successful(self):
        code = self.session.query(Users).filter(Users.email == "newuser@example.com").first().auth_code
        response = verify(code, self.token, self.session)
        self.assertIsInstance(response, NoContent)

    def test_verify_returns_bad_request_if_code_wrong(self):
        response = verify("WRONG1", self.token, self.session)
        self.assertIsInstance(response, BadRequest)

    def test_change_email_returns_accepted_response_if_successful(self):
        response = change_email("new_email@example.com", self.token, self.session)
        self.assertIsInstance(response, NoContent)

    def test_change_email_returns_conflict_if_email_exists(self):
        response = change_email("newuser@example.com", self.token, self.session)
        self.assertIsInstance(response, Conflict)
    def test_change_password_returns_accepted_response_if_successful(self):
        response = change_password("new_password", self.token, self.session)
        self.assertIsInstance(response, NoContent)

    def test_delete_returns_accepted_response_if_successful(self):
        response = delete(self.token, self.session)
        self.assertIsInstance(response, Accepted)

if __name__ == "__main__":
    # Define a custom sorting function for test methods
    def custom_sort(test_case, method):
        test_order = [
            test_case.test_register_returns_created_response_if_successful,
            test_case.test_try_login_returns_false_if_credentials_do_not_match,
            test_case.test_try_login_returns_user_object_if_credentials_match,
            test_case.test_create_token_returns_string,
            test_case.test_verify_returns_accepted_response_if_successful,
            test_case.test_change_email_returns_accepted_response_if_successful,
            test_case.test_change_password_returns_accepted_response_if_successful,
            test_case.test_delete_returns_accepted_response_if_successful,
        ]
        return test_order.index(method)

    # Set the custom sorting function for the test loader
    unittest.TestLoader.sortTestMethodsUsing = custom_sort

    unittest.main()