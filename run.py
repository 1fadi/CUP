from webdriver import Simulator
import os


def main():
    simulator = Simulator(
        reddit_username=os.environ.get("REDDIT_USERNAME"),
        reddit_password=os.environ.get("REDDIT_PASSWORD"),
        verbose=False,
        hidden=False
    )
    simulator.run_()


if __name__ == "__main__":
    main()
