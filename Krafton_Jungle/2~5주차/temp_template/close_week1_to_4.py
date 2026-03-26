#!/usr/bin/env python3
import requests
import sys
import time
from secrets import GITHUB_TOKEN, REPO_OWNER, REPO_NAME

def main():
    print(f"🔍 1~4주차 이슈 닫기 시작 (대상 레포: {REPO_OWNER}/{REPO_NAME})")
    
    headers = {
        'Authorization': f'token {GITHUB_TOKEN}',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    page = 1
    closed_count = 0
    
    while True:
        url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues'
        params = {'state': 'open', 'per_page': 100, 'page': page}
        
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            print(f"❌ 이슈 목록 가져오기 실패: {response.status_code}")
            break
            
        issues = response.json()
        if not issues:
            break
            
        for issue in issues:
            # PR 제외
            if 'pull_request' in issue:
                continue
                
            title = issue.get('title', '')
            # 1~4주차인지 확인
            is_target = False
            for w in [1, 2, 3, 4]:
                if f'[WEEK{w}]' in title:
                    is_target = True
                    break
                    
            if is_target:
                issue_number = issue['number']
                patch_url = f'https://api.github.com/repos/{REPO_OWNER}/{REPO_NAME}/issues/{issue_number}'
                # 프로젝트 보드에서 완료로 뜨지 않도록 state_reason 값을 not_planned로 시도해 봅니다.
                # (프로젝트 워크플로우 설정에 따라 그래도 이동할 수 있음)
                patch_data = {'state': 'closed', 'state_reason': 'not_planned'}
                
                res = requests.patch(patch_url, headers=headers, json=patch_data)
                if res.status_code == 200:
                    print(f"✅ 닫힘: #{issue_number} {title}")
                    closed_count += 1
                else:
                    print(f"❌ 실패 (HTTP {res.status_code}): #{issue_number} {title}")
                
                time.sleep(1.0) # API 제한 방지
                
        page += 1

    print(f"✨ 총 {closed_count}개의 1~4주차 이슈를 닫았습니다.")

if __name__ == "__main__":
    main()
