from typing import List

from app.core.deployers.deployer import BaseDeployer, PreExecContext, ExecContext, PostExecContext


class SampleDeployer(BaseDeployer):

    @staticmethod
    def deployer_pre_exec_jobs() -> List[str]:
        return ['pre_1', 'pre_2']

    @staticmethod
    def deployer_exec_jobs() -> List[str]:
        return ['e_1', 'e_2']

    @staticmethod
    def deployer_post_exec_jobs() -> List[str]:
        return ['post_1', 'post_2']

    @staticmethod
    def check_prerequisite() -> bool:
        print("Test: requirements check!")
        return True

    @staticmethod
    def pre_1(context: PreExecContext):
        print(f'context: {context.step} started@{context.started}')

    @staticmethod
    def pre_2(context: PreExecContext):
        print(f'context: {context.step} started@{context.started}')

    @staticmethod
    def e_1(context: ExecContext):
        print(f'context: {context.step} started@{context.started}')

    @staticmethod
    def e_2(context: ExecContext):
        print(f'context: {context.step} started@{context.started}')

    @staticmethod
    def post_1(context: PostExecContext):
        print(f'context: {context.step} started@{context.started}')

    @staticmethod
    def post_2(context: PostExecContext):
        print(f'context: {context.step} started@{context.started}')
