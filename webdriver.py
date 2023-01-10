from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from exceptions import ContinueException
import time


class Simulator(webdriver.Firefox):

    def __init__(self,
        reddit_username,
        reddit_password,
        verbose=False,
        hidden=False
    ):
        super().__init__()
        self._reddit_username = reddit_username
        self._reddit_password = reddit_password
        self._verbose = verbose
        self._hidden = hidden

        if self._hidden:
            _options = webdriver.firefox.options.Options()
            _options.add_argument("--headless")
            self.options = _options
    
    def run_(self):
        self._login_to_site()
        time.sleep(14)
        self._get_page(
            f"https://www.reddit.com/user/{self._reddit_username}/comments")
        comments_deleted = 0
        while True:
            time.sleep(0.7)
            try:
                process = self._delete_comment()
                if process == "Deleted comment":
                    if self._verbose:
                        comments_deleted =+ 1
                        print(f"Deleted a comment")
                    else:
                        pass
            except KeyboardInterrupt:
                break
                if self._verbose:
                    print("number of comments deleted: {comments_deleted}")
            except ContinueException:
                continue

        self.stop_()
        if self._verbose:
            print(f"number of comments deleted: {comments_deleted}")

    def stop_(self):
        try:
            self.quit()
        except Exception as err:
            exit("exited with error", err)

    def _try_condition(self, condition, sec=10, **kwargs):
        return WebDriverWait(self, sec).until(condition(**kwargs))

    def _get_page(self, url):
        try:
            self.get(url)
        except Exception as err:
            self.stop_()
            return err

    def _login_to_site(self):
        self._get_page("https://www.reddit.com/login/")
        time.sleep(3)
        # locate username section
        username_input = self.find_element(By.ID, "loginUsername")
        username_input.clear()
        username_input.send_keys(self._reddit_username)
        # locate password section
        password_input = self.find_element(By.ID, "loginPassword")
        password_input.clear()
        password_input.send_keys(self._reddit_password)
        # submit results
        submit = self.find_element(By.CLASS_NAME, "AnimatedForm__submitButton")
        submit.click()

    def _delete_comment(self):
        try:
            comment_options = self._try_condition(
                sec=5,
                condition=EC.presence_of_element_located,
                locator=(By.CLASS_NAME, "_2pFdCpgBihIaYh9DSMWBIu")
            )
            comment_options = self._try_condition(
                sec=5,
                condition=EC.element_to_be_clickable,
                mark=(By.CLASS_NAME, "_2pFdCpgBihIaYh9DSMWBIu")
            )
        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            # raise Exception()
            raise ContinueException()

        comment_options.click()
        comment_dropdown = self._try_condition(
            sec=5,
            condition=EC.presence_of_all_elements_located,
            locator=(By.CLASS_NAME, "_10K5i7NW6qcm-UoCtpB3aK")
        )
        self._try_condition(
            condition=EC.visibility_of,
            element=comment_dropdown[0]
        )
        options = self._try_condition(
            condition=EC.presence_of_all_elements_located,
            locator=(By.CLASS_NAME, "_10K5i7NW6qcm-UoCtpB3aK")
        )
        self._try_condition(
            condition=EC.visibility_of,
            element=options[0]
        )
        try:
            options[4].click()
            popup_options = self._try_condition(
                sec=2,
                condition=EC.presence_of_all_elements_located,
                locator=(By.CLASS_NAME, "_2nelDm85zKKmuD94NequP0")
            )
            for option in popup_options:
                if option.text == "Delete":
                    option.click()
                    if self._verbose:
                        return "Deleted comment"

        except KeyboardInterrupt:
            raise KeyboardInterrupt()
        except:
            raise ContinueException()

