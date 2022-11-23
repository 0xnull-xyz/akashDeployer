import inspect
import os
import sys
from abc import ABC, abstractmethod
from datetime import datetime
from itertools import chain
from typing import List

from celery import shared_task


class AbstractDeployer(ABC):

    @abstractmethod
    def deployer_pre_exec_jobs(self) -> List[str]:
        pass

    @abstractmethod
    def deployer_exec_jobs(self) -> List[str]:
        pass

    @abstractmethod
    def deployer_post_exec_jobs(self) -> List[str]:
        pass

    @abstractmethod
    def check_prerequisite(self) -> bool:
        print("requirements check!")

    @staticmethod
    @abstractmethod
    def deploy(self):
        print("deploy!")


class PreExecContext:
    def __init__(self, step):
        self.step = step
        self.started = datetime.now()


class ExecContext:
    def __init__(self, step):
        self.step = step
        self.started = datetime.now()


class PostExecContext:
    def __init__(self, step):
        self.step = step
        self.started = datetime.now()


class BaseDeployer(AbstractDeployer, ABC):

    def deployer_pre_exec_jobs(self) -> List[str]:
        return []

    def deployer_exec_jobs(self) -> List[str]:
        return []

    def deployer_post_exec_jobs(self) -> List[str]:
        return []

    @staticmethod
    def check_prerequisite() -> bool:
        print("requirements check!")
        return True

    @staticmethod
    @shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, retry_kwargs={"max_retries": 5},
                 name='deployers:deploy')
    def deploy(self, deployer_id: str, deployment_id: str):
        dir_path = os.path.dirname(os.path.realpath(__file__)) + os.sep
        for module in os.listdir(os.path.dirname(dir_path)):
            if module == '__init__.py' or module[-3:] != '.py' or module == str(__file__).removeprefix(dir_path):
                continue
            __import__(f'app.core.deployers.{module[:-3]}', locals(), globals())
        del module

        deployers_modules = [m for _, m in inspect.getmembers(sys.modules['app.core.deployers'], inspect.ismodule)]
        cls_members = list(chain.from_iterable([inspect.getmembers(m, inspect.isclass) for m in deployers_modules]))
        deployer = next(filter(lambda c: c[0] == deployer_id, cls_members))[1]
        check_method = getattr(deployer, 'check_prerequisite')
        check_prerequisite_res = check_method()
        if check_prerequisite_res:
            pre_jobs = getattr(deployer, 'deployer_pre_exec_jobs')
            pre_exec_context = PreExecContext(0)
            for job in pre_jobs():
                pre_exec_job = getattr(deployer, job)
                pre_exec_job(pre_exec_context)
                pre_exec_context.step += 1

            exec_jobs = getattr(deployer, 'deployer_exec_jobs')
            exec_context = ExecContext(0)
            for job in exec_jobs():
                exec_job = getattr(deployer, job)
                exec_job(exec_context)
                exec_context.step += 1

            post_jobs = getattr(deployer, 'deployer_post_exec_jobs')
            post_exec_context = PostExecContext(0)
            for job in post_jobs():
                post_exec_job = getattr(deployer, job)
                post_exec_job(post_exec_context)
                post_exec_context.step += 1
        else:
            raise RuntimeError(f'{type(deployer).__name__} deploy failed! Check Prerequisites Failed!')
