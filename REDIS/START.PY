import redis

# Redis 서버에 연결 (기본 포트 6379)
# decode_responses=True : 바이트가 아닌 문자열로 받기
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# ① 연결 확인: True가 출력되면 성공
print(r.ping())  # 출력: True

# ② 데이터 저장: SET hello "world"와 동일
r.set('hello', 'world')

# ③ 데이터 조회: GET hello와 동일
value = r.get('hello')
print(value)  # 출력: world

# ④ TTL(만료 시간) 설정: 10초 후 자동 삭제
r.set('session:user1', 'logged_in', ex=10)
print(r.ttl('session:user1'))  # 출력: 10 (초 단위 남은 시간)