Hydro
=====

Hydro is a free and open source Data API computation and serving framework, which designed mainly to help web/application servers or other data consumers to extract data from different data streams, process it on the fly and render it to different clients/applications based on criteria and statistics.

```

           |-------|
           |  DB1  |======
           |-------|     =
               .         =      Data API           
                         =    |-----------|        
               .         = >  | HYDRO -   |        |---------|        
                         =    | Extract   |        | APP/Web |        |--------|
===ETL===>     .         =    | Transform | =====> | Server  | =====> | Client |     
                         = >  | Render    |        |---------|        |--------|
               .         =    |-----------|                       
                         =                         
           |-------|     =
           |  DBn  |====== 
           |-------|


```

## Hydro makes it easy to:

1. Consolidate into **one service** a logic of processing different types of inbound streams from [speed and batch](http://lambda-architecture.net/) layers.
2. Optimize data retrieval by performing various types of optimization and transformation techniques during run time such as:
  * Sampling.
  * Deciding on data access path (pre materialized / raw data).
  * Data streams operations:  lookup-ing, aggregations, computed columns and etc.
  * Resource allocation per user/query/client/QOS.
3. Create multi level caching.
4. Reuse and share business logic across different consumers and data streams.

Hydro is built in a way that data/biz logic is separated from data extraction, in that way Hydro can define different data structures to extract data from **but** apply the same processing logic, once data is fetched.  


##  Building blocks:

**Topology:**

Topology is a definition of a processing logic:

* Defining the input data streams
* Operations on data streams
* Rendering the output 

Example:

```
#defining main stream
main_stream = self.query_engine.get('geo_widget_stream', params)

#defining lookup stream
lookup_stream = self.query_engine.get('geo_lookup_stream', params, cache_ttl=1)

#combining 2 streams based on field user_id for both stream
combined = self.transformers.combine(main_stream, lookup_stream, left_on=['user_id'], right_on=['user_id'])

#aggregating by 'country' and create 2 computed columns for the summary of 'revenue' and 'spend'
aggregated = self.transformers.aggregate(combined, group_by=['country'], operators={'revenue': 'sum', 'spend': 'sum'})

#creating computed column for calculating ROI
aggregated['ROI'] = aggregated.revenue/(aggregated.spend+aggregated.revenue)

#returning the data set
return aggregated
```

**Query Engine**

Query engine is responsible of connecting to data source and extract data from it.
the query engine is utilizing the Optimizer in order to determine the access path, data structures and optimization logic in order to tap the stream.

**Optimizer**

Optimizer is responsible of applying optimization techniques in order to fetch a stream in the most efficient way based on criteria and statistics. Optimizer returns a plan for the Query Engine to follow.

Example:

```
#creating a plan object
plan = PlanObject(params, source_id, conf)
# defining data source and type
plan.data_source = 'vertica-dash'
plan.source_type = Configurator.VERTICA

# time diff based on input params
time_diff = (plan.TO_DATE - plan.FROM_DATE).total_seconds()

# if time range is bigger than 125 days and application type is dashboard, abort! 
# since data need to be fetched quickly
if time_diff > Configurator.SECONDS_IN_DAY*125 and params['APP_TYPE'].to_string() == 'Dashboard':
	raise HydroException('Time range is too big')

# else, if average records per day is bigger than 1000 or client is convertro then run sample logic
elif plan.AVG_RECORDS_PER_DAY > 1000 or params['CLIENT_ID'].to_string() == 'convertro':
	plan.template_file = 'device_grid_widget_sampling.sql'
	plan.sampling = True
	self.logger.debug('Sampling for the query has been turn on')

# else run other logic
else:
	plan.template_file = 'device_grid_widget.sql'
#return plan object to the query engine
return plan

```

**Caching**

Hydro is using stream and topology based caching, in order to boost performance, in a case the same stream/topology and parameters where fetched before. Streams and topologies can be shared across topologies and in fact, topology can be yet another stream for other topology.


##  How to use:
Using Hydro usually involves the following steps:

1. Installation with `pip install hydro`
2. Generating a topology with `hydro_cli scaffold [dir_name] [TopologyName]`
3. Editing the generated files and filling in the logic and queries.
4. Invoke Hydro locally or remotely as explained below.


## Contributing
We are accepting pull requests.

In order to set-up a development environment, all you have to do is to clone this project and run `pip install -r requirements.txt`.
We strongly recommend using virtualenv in order to avoid the dependencies pollute the system's Python installation.