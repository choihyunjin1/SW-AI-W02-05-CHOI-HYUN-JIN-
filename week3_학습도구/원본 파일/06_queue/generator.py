from collections import deque

class QueueGenerator:
    def __init__(self, jobs):
        self.jobs = jobs
        
    def generate(self):
        # INIT_CODE
        code = [
            "from collections import deque",
            "",
            "def process_print_queue(jobs):",
            "    queue = deque(jobs)",
            "    processed = []",
            "    ",
            "    while queue:",
            "        job = queue.popleft()",
            "        print(f'처리: {job}')",
            "        processed.append(job)",
            "        ",
            "    return processed"
        ]
        
        yield "INIT_CODE", code, -1, "초기화: 프린터 대기열 처리 코드를 불러왔습니다."
        
        queue = deque()
        processed = []
        
        yield "INIT_VARS", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 3, "초기 변수를 준비합니다."
        
        # deque(jobs) 모사
        for job in self.jobs:
            queue.append(job)
            yield "ENQUEUE_INIT", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 3, f"초기화: 문서 '{job}' 를 대기열(Queue)에 넣습니다(Enqueue)."
            
        yield "CHECK_WHILE", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 6, f"반복 검사: 대기열 큐(Queue)에 대기 중인 작업이 1개라도 있는가?"
        
        while queue:
            yield "DEQUEUE_PRE", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 7, "큐의 가장 앞(Left)에서 작업을 꺼냅니다(Dequeue/popleft)."
            
            job = queue.popleft()
            yield "DEQUEUE_DONE", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": job}, 7, f"작업 '{job}' 을(를) 큐에서 꺼냈습니다."
            
            yield "PROCESS_PRINT", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": job}, 8, f"프린터 출력 수행: '{job}' 인쇄 중..."
            
            processed.append(job)
            yield "PROCESS_DONE", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": job}, 9, f"출력 완료: '{job}' 을(를) 완료 목록에 추가합니다."
            
            yield "CHECK_WHILE", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 6, f"반복 검사: 대기열 큐(Queue)에 다음 작업이 존재하는가?"

        yield "FINISHED", {"jobs": self.jobs, "queue": list(queue), "processed": processed.copy(), "current_job": None}, 11, "완료: 큐가 비어있으므로 모든 프린터 작업 처리를 완료하고 결과를 반환합니다."


def queue_generator(jobs):
    gen = QueueGenerator(jobs)
    return gen.generate()
