Elasticsearch 쿼리 알림 설정
======

## 소개
엘라스틱서치에서 원하는 쿼리 결과를 슬랙 등으로 알림을 하기 위한 라이브러리

### <a name="디렉토리-구성"></a>디렉토리 구성
    .
    ├── conf   # 기본 설정 파일 폴더
    │   ├── config.ini    # elastic,slack url 설정
    │   └── rules.ini     # ./rules/*.json 폴더 파일들과 연결 설정
    ├── libs  # 소스 파일
    ├── rules  # 검색 쿼리 룰 파일
    └── tests  # unit tests

### <a name="기본 설정"></a>기본 설정
- conf/config.ini
```ini
[elastic]
url = https://<elasticsearch:9200> #elasticsearch https URL 입력
ApiKey = <APIKEY>  # apikey 설정

[slack]
url = https://hooks.slack.com/services/<AAAA/BBBBBB/xZVCqbWzHoYwlVdJFv5rdd9P> # 슬랙 알림 API URL 설정
```

### <a name="룰 설정"></a>룰 설정
- conf/rules.ini
```ini
[disk_full]  #이 항목을 ./rules/<disk_full>.json 폴더에서 찾는다
search_path = /logstash_metricbeat_*/_search
notify_key = hits.hits.fields.timestamp.0,hits.hits._source.host.name,hits.hits.fields.pct.0,hits.hits.fields.available.0,hits.hits._source.system.filesystem.device_name,hits.hits._source.system.filesystem.mount_point
notify_format = Time:{0}, Host: {1}, Device: {4}, Path: {5}, Usable: {2}, Available: {3}
notify_title = Disk Full Alert
```
- search_path : query 검색할 path
- notify_key : 검색 결과 json 파일에서 알럿 전송할 항목
- notify_format : 위 항목에서 설정한 필드를 매칭시켜 Alert 전송 메시지로 변환할 포맷
- notify_title : Alert 타이틀

### <a name="테스트"></a>테스트
```bash
-- elastic 접속 및 query 테스트
$ python3 -m unittest tests/libs/elastic.py
-- rules 설정 테스트
$ python3 -m unittest tests/libs/rules.py
-- slack 알림 테스트
$ python3 -m unittest tests/libs/slack.py
```

### <a name="사용법"></a>사용법 1
룰 설정후 실행
```bash
$ python3 main.py
```
