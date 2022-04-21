This file contains how to set up the docker on linux.

First open terminal to where the files are.

Execute commands in this order:

```
docker-compose up -d
```

```
docker exec -it hive-server /bin/bash
```

```
cd ..
```

```
cd episode
```

```
hive -f episode_table.hql
```

```
hadoop fs -put CleanEpisodes.csv hdfs://namenode:8020/user/hive/data/episodesdb.db/episode
```

```
hive
```

```
use episodesdb;
```

```
ALTER TABLE episode
SET TBLPROPERTIES ("skip.header.line.count"="1");
```

You can use this commmand to view the items

```
select * from episode limit 10;
```

Now the docker image should be initialised onto your system!
