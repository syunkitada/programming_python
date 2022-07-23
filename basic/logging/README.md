# Logging

- ロギングのために、print と import logging は使ってはいけない
- ロギングには getLogger を利用する
- コンソール出力のためにだけ print は使う

```python
from logging import getLogger, StreamHandler, DEBUG
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(DEBUG)
logger.setLevel(DEBUG)
logger.addHandler(handler)

logger.debug('start')
```

## Reference

- http://qiita.com/amedama/items/b856b2f30c2f38665701
