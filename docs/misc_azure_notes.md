# Azure Databricks
_Notes concerning Azure and Databricks concepts._

## What is Azure Databricks?
A data analytics platform optimized for the Azure cloud. It offers **two environments** for developing data intensive applications:
1. **Asure Databricks SQL Analytics**: Provides easy-to-use platform for analsts who want to run SQL queries on their data lake, create visualizations to explore query results, and build and share dashboards.
2. **Azure Databricks Workspace**: Interactive workspace that enables collaboration between data engineers, data scientists and machine learning engineers. For a Big Data pipeline, the data (raw or unstructured) is ingested into Azure through Azure Data Factory (ADF) batches or streamed near real-time using Kafka, Event Hub or IoT Hub. This data lands in a data lake for long term persistent storage in Azure Blob Storage or Azure Data Lake Storage. As part of the analytics workflow, use Azure Databricks to read data from sources and turn them into insights using Spark.

## Azure Databricks Architecture
- The [overlaying architecture](https://docs.microsoft.com/en-us/azure/databricks/getting-started/overview) aims for individuals and teams to focus on data science, analytics and engineering tasks by using managed services available through Azure Databricks.
- Azure Databricks operates out of a **control plane** and a **data plane**.
- **Control Plane**: This includes the backend services that Azure Databricks manages in its own Azure account. Any commands that you run will exist in the control plane with your code fully encrypted (_**Note**: Saved commands reside in the Data Plane_).
- **Data Plane**: Where your data resides and is processed assuming the data has already been ingested into Databricks. You can connect streaming, IoT, event data and more here while also connecting **external data** sources outside of Azure [**using Databrick connectors**](https://docs.microsoft.com/en-us/azure/data-factory/connector-overview). Your data always resides in your Azure account in the data plane, not the control plane, so you always maintain full control and ownership of your data without lock-in.

## Azure Databricks Workspace
Azure Databricks Workspace is an analytics platform based on Apache Spark. Azure Databricks Workspace is integrated with Azure to provide one-click setup, streamlined workflows, and an interactive workspace that enables collaboration between data engineers, data scientists, and machine learning engineers. The notes below were was derived from [Microsoft's Azure Documentation](https://docs.microsoft.com/en-us/azure/databricks/scenarios/what-is-azure-databricks-ws).

### Term Glossary

#### Workspace
- **Workspace**: Environment for accessing all of the Databricks assets. A workplace organizes objects (notebooks, libraries, dashboards and experiments) into [folders](https://docs.microsoft.com/en-us/azure/databricks/workspace/workspace-objects#folders) and provides access to data objects and computational resources.
- **Notebook**: Web-based interface to documents that contain runnable commands, visualizations and narrative text (think of a Cloud Jupyter Notebook).
- **Dashboard**: An interface that provides access to visualizations.
- **Library**: Package of code available to the notebook or job running on the cluster. The Databricks runtime includes many libraries and you are free to add your own as well.
- **Experiment**: Collection of [MLFlow](https://docs.microsoft.com/en-us/azure/databricks/applications/mlflow/tracking#mlflow-tracking) runs for training and machine learning models. More information on this concept is outlined in the documentation below.
- **Folders**: Contain all static assets within a workspace including: notebooks, libraries, experiments and other folders.
  - The Workspace root folder is a container for all of your organization’s Azure Databricks static assets.
  - **Shared** is for sharing objects across the organization and all users have full permissions for objects in this folder.
  - **Users** contains a folder for each user.
  - By default, the Workspace root folder and all of its contained objects are available to all users. You can control who can manage and access objects by [enabling workspace access control](https://docs.microsoft.com/en-us/azure/databricks/administration-guide/access-control/workspace-acl#enable-workspace-acl) and [setting permissions](https://docs.microsoft.com/en-us/azure/databricks/security/access-control/workspace-acl#permissions).

#### Interface
- **UI**: An easy-to-use graphical interface to workspace folders and their contained objects, data objects, and computational resources.
- **REST API**: There are two versions of the REST API: REST API 2.0 and REST API 1.2. The REST API 2.0 supports most of the functionality of the REST API 1.2, as well as additional functionality and is preferred.
- **Command Line Interface (CLI)**: An [open-source tool](https://github.com/databricks/databricks-cli) which provides an easy to use interface to the Databricks platform. The CLI is built on top of the Databricks REST APIs. **NOTE**: This CLI is **under active development** and is released as an experimental client. This means that interfaces are still subject to change.

#### Data Management
- **Databricks File System (DBFS)**: A filesystem abstraction layer over a blob store. It contains directories, which can contain files (data files, libraries, and images), and other directories. DBFS is automatically populated with some [datasets](https://docs.microsoft.com/en-us/azure/databricks/data/databricks-datasets) that you can use to learn Azure Databricks.
- **Database**: Collection of information that is organized so that it can be easily accessed, managed and updated.
- **Table**: Representation of structured data that are queried using Spark.
- **Metastore**: The component that stores all the structure information of the various tables and partitions in the data warehouse including column and column type information, the serializers and deserializers necessary to read and write data, and the corresponding files where the data is stored. Every Azure Databricks deployment has a central Hive metastore accessible by all clusters to persist table metadata. You also have the option to use an existing [external Hive metastore](https://docs.microsoft.com/en-us/azure/databricks/data/metastores/external-hive-metastore).

#### Computation Management
- **Cluster**: A set of computation resources and configurations on which you run notebooks and jobs. There are **two types of clusters**: _**all-purpose**_ and _**job**_.
  1. **All-Purpose Cluster**: You create an all-purpose cluster using the UI, CLI, or REST API. You can **manually terminate and restart an all-purpose cluster**. Multiple users can share such clusters to do collaborative interactive analysis.
  2. **Job Cluster**: Azure Databricks job scheduler creates a job cluster when you run a job on a new job cluster and terminates the cluster when the job is complete. You **cannot restart** a job cluster.
- **Pool**: Set of idle, ready-to-use instances that reduce cluster start and auto-scaling times. When attached to a pool, a cluster allocates its driver and worked nodes from the pool. If the pool does not have sufficient idle resources to accommodate the cluster's request, the pool expands by allocating new instances from the instance provider. When an attached cluster is terminated, the instances it used are returned to the pool and can be reused by a different cluster.
- **Databricks Runtime**: _This is outlined further below_.
- **Job**: Non-interactive mechanism for running a notebook or library either immediately or on a scheduled basis.
  - **Workload**: Azure Databricks identifies two types of workloads subject to different pricing schemes: data engineering (job) and data analytics (all-purpose).
    - **Data Engineering**: An _(automated)_ workload runs on a job cluster which the Azure Databricks job scheduler creates for each workload.
    - **Data Analytics**: An _(interactive)_ workload runs on an all-purpose cluster. Interactive workloads typically run commands within an Azure Databricks notebook. However, running a job on an existing all-purpose cluster is also treated as an interactive workload.
  - **Execution Context**: The state for a REPL (Read–Eval–Print Loop) environment for each supported programming language. The languages supported are Python, R, Scala, and SQL.

#### Model Management
- **Model**: A mathematical function that represents the relationship between a set of predictors and an outcome. Machine learning consists of training and inference steps. You train a model using an existing dataset, and then use that model to predict the outcomes (inference) of new data.
  - The ability to **Log, load, register, and deploy MLflow Models** can be done a number of ways and is outlined in their [documentation](https://docs.microsoft.com/en-us/azure/databricks/applications/mlflow/models).
- **Run**: A collection of parameters, metrics, and tags related to training a machine learning model.
- **Experiment**: The primary unit of organization and access control for runs; all MLflow runs belong to an experiment. An experiment lets you visualize, search, and compare runs, as well as download run artifacts or metadata for analysis in other tools. **There are two types of experiments**: _**workspace**_ and _**notebook**_.
  1. You can create a **workspace experiment** from the Workspace UI or the MLflow API. Workspace experiments are not associated with any notebook, and any notebook can log a run to these experiments by using the experiment ID or the experiment name.
  2. A **notebook experiment** is associated with a specific notebook. Azure Databricks automatically creates a notebook experiment if there is no active experiment when you start a run using `mlflow.start_run()`.
    - **NOTE**: If you delete a notebook experiment using the API (for example, `MlflowClient.tracking.delete_experiment()` in Python), the notebook itself is moved into the Trash folder.
  - **Log MLflow Runs**: You can use MLflow Python, Java or Scala, and R APIs to start runs and record run data.
  - **Viewing, Managing, Downloading and Comparisons of Runs** are all possible and can be done with relative ease.
  - **Analyze MLflow Runs Using DataFrames**: You can access MLflow run data programmatically using the following two DataFrame APIs:
    - The MLflow Python client `search_runs` [API](https://mlflow.org/docs/latest/python_api/mlflow.html#mlflow.search_runs) returns a pandas DataFrame.
    - The [MLflow experiment](https://docs.microsoft.com/en-us/azure/databricks/data/data-sources/mlflow-experiment#mlflow-exp-datasource) data source returns an Apache Spark DataFrame.

### Apache Spark Analytics Platform
Azure Databricks Workspace comprises the complete open-source Apache Spark cluster technologies and capabilities. Spark in Azure Databricks Workspace includes the following components:
- **Spark SQL and DataFrames**: Spark SQL is the Spark module for working with structured data. A DataFrame is a distributed collection of data organized into named columns. It is conceptually equivalent to a table in a relational database or a data frame in R/Python.
- **Streaming**: Real-time data processing and analysis for analytical and interactive applications. Integrates with HDFS, Flume, and Kafka.
- **MLlib**: Machine Learning library consisting of common learning algorithms and utilities, including classification, regression, clustering, collaborative filtering, dimensionality reduction, as well as underlying optimization primitives.
- **GraphX**: Graphs and graph computation for a broad scope of use cases from cognitive analytics to data exploration.
- **Spark Core API**: Includes support for R, SQL, Python, Scala, and Java.
  - We use Python for the BCO Retention Project. Although the gap between Python and JVM based language such as Scala and Java are slimming in terms of execution speed. If we shifted to using a JVM language it would provide the best performance but at this time is a non-issue.

#### Apache Spark in Azure Databricks Workspace
Azure Databricks Workspace builds on the capabilities of Spark by providing a zero-management cloud platform that includes:
- **Fully Managed Spark Clusters**: Azure Databricks has a secure and reliable production environment in the cloud, managed and supported by Spark experts
  - Create clusters in seconds.
  - Dynamically autoscale clusters up and down and share them across teams.
  - Use clusters programmatically by invoking REST APIs.
  - Use secure data integration capabilities built on top of Spark that enable you to unify your data without centralization.
  - Get instant access to the latest Apache Spark features with each release.
- An interactive workspace for **exploration and visualization**.
- A platform for powering your favorite **Spark** applications.

### Databricks Runtime
Databricks Runtime is built on top of Apache Spark and is natively built for the Azure cloud.
Azure Databricks **completely abstracts out the infrastructure complexity** and the need for specialized expertise to set up and configure your data infrastructure. For data engineers, who care about the performance of production jobs, Azure Databricks provides a **Spark engine that is faster and performant through various optimizations** at the I/O layer and processing layer (Databricks I/O).
- This is one of the drivers behind upgrading the Runtime for Phase 2 of the BCO engagement.
- Potentially will upgrade to [Azure Databricks 7.3 Long Term Support (LTS)](https://docs.microsoft.com/en-us/azure/databricks/release-notes/runtime/7.3)

The set of core components that run on the clusters managed by Azure Databricks. Azure Databricks offers several types of runtimes:
- **Databricks Runtime** includes Apache Spark but also adds a number of components and updates that substantially improve the usability, performance, and security of big data analytics.
- **Databricks Runtime for Machine Learning** is built on Databricks Runtime and provides a ready-to-go environment for machine learning and data science. It contains multiple popular libraries, including TensorFlow, Keras, PyTorch, and XGBoost.
- **Databricks Runtime for Genomics** is a version of Databricks Runtime optimized for working with genomic and biomedical data.
- **Databricks Light** is the Azure Databricks packaging of the open source Apache Spark runtime. It provides a runtime option for jobs that don’t need the advanced performance, reliability, or autoscaling benefits provided by Databricks Runtime. You can select Databricks Light only when you create a cluster to run a JAR, Python, or spark-submit job; you cannot select this runtime for clusters on which you run interactive or notebook job workloads.

## Azure Data Factory
Azure Data Factory is Azure's cloud ETL service for scale-out serverless data integration and data transformation. Full documentation concerning Azure Data Factory (ADF) can be found [here](https://docs.microsoft.com/en-us/azure/data-factory/).

## Azure to AWS Equivelance
_Equivalence's between Azure and Amazon Web Service (AWS) offerings._
### Common Services
- [Azure Virtual Machines (VM)](https://azure.microsoft.com/en-us/services/virtual-machines/) is equivalent to [Amazon Elastic Compute Cloud (EC2)](https://aws.amazon.com/ec2/): Virtual servers allow users to deploy, manage, and maintain OS and server software. Instance types provide combinations of CPU/RAM. Users pay for what they use with the flexibility to change sizes.
- [Azure Blob Storage](https://docs.microsoft.com/en-us/azure/storage/blobs/storage-blobs-introduction) is equivalent to [AWS Simple Storage Service (S3)](https://aws.amazon.com/s3/): Object storage service, for use cases including cloud applications, content distribution, backup, archiving, disaster recovery, and big data analytics.
- [Azure Virtual Disks](https://docs.microsoft.com/en-us/azure/virtual-machines/managed-disks-overview) is equivalent to [AWS Elastic Block Storage (EBS)](https://aws.amazon.com/ebs/?ebs-whats-new.sort-by=item.additionalFields.postDateTime&ebs-whats-new.sort-order=desc): Block storage divides your files into equally-sized pieces. This allows users to change just a small piece of the data, and do so quickly. The blocks are always connected to a cloud server, such as Azure VM or Amazon EC2. They store the OS to boot up the virtual server.
- [Azure Virtual Machine Scaling](https://docs.microsoft.com/en-us/azure/virtual-machine-scale-sets/virtual-machine-scale-sets-overview) is equivalent to [AWS Auto Scaling](https://aws.amazon.com/autoscaling/): This allows you to automatically change the number of VM instances. You set defined metric and thresholds that determine if the platform adds or removes instances.
- [Azure Functions](https://azure.microsoft.com/services/functions/) are equivalent to [AWS Lambda](https://aws.amazon.com/lambda/): This service integrates systems and run backend processes in response to events or schedules without provisioning or managing servers.

### Data and Analytics
- [AWS Elastic Map Reduce (EMR)](https://aws.amazon.com/emr) vs. [Azure Big Data Processing Services](https://docs.microsoft.com/en-us/azure/architecture/aws-professional/services#big-data-and-analytics): AWS EMR encompasses many components that are provided individually through Azure, these include:
  - [Azure Data Explorer](https://azure.microsoft.com/services/data-explorer/): Fully managed, low latency, distributed big data analytics platform to run complex queries across petabytes of data.
  - [Databricks](https://azure.microsoft.com/services/databricks/): Apache Spark based analytics platform.
  - [HDInsight](https://azure.microsoft.com/services/hdinsight/): Managed Hadoop service for deploying and managing Hadoop clusters.
  - [Data Lake Storage](https://azure.microsoft.com/services/storage/data-lake-storage/): Massively scalable, secure data lake functionality built on Azure Blob Storage.
- [PowerBI](https://powerbi.microsoft.com/) is equivalent to [AWS QuickSight](https://aws.amazon.com/quicksight/): Business intelligence tools that build visualizations, perform ad hoc analysis, and develop business insights from data.
- [Data Lake Analytics](https://azure.microsoft.com/services/data-lake-analytics/) is equivalent to [AWS Athena](https://aws.amazon.com/athena/): Provides a serverless interactive query service that uses standard SQL for analyzing databases.

### Database
- **Azure Relational Databases (RDBMS)** including [SQL Database](https://azure.microsoft.com/services/sql-database/), [MySQL](https://azure.microsoft.com/services/mysql/) and [PostgreSQL](https://azure.microsoft.com/services/postgresql/) are equivalent to [AWS RDS](https://aws.amazon.com/rds/). These are managed relational database service where resiliency, scale, and maintenance are primarily handled by the platform.
- **NoSQL/Document Database** in Azure are encompassed together in [Cosmos DB](https://azure.microsoft.com/services/cosmos-db/) while AWS equivalent service offerings include [DynamoDB](https://aws.amazon.com/dynamodb/), [SimpleDB](https://aws.amazon.com/simpledb/) and [Amazon DocumentDB](https://aws.amazon.com/documentdb/). Theses are globally distributed, multi-model database that natively supports multiple data models: key-value, documents, graphs, and columnar.
- **Caching** in Azure is done with [Cache for Redis](https://azure.microsoft.com/services/cache/) while the AWS equivalent is [ElastiCache](https://aws.amazon.com/elasticache/). These offer an in-memory–based, distributed caching service that provides a high-performance store typically used to offload non-transactional work from a database.

## Azure Subscription
- **Subscription**: Essentially, subscriptions are a named container for a pair of subscription keys. Developers who need to consume the published APIs can get subscriptions for access to these APIs.
- **Scope of Subscriptions** : Subscriptions can be associated with various scopes: product, all APIs, or an individual API.
- **Use Cases**
  - When you publish APIs through API Management, it's easy and common to secure access to those APIs by using subscription keys.
  - Traditionally, subscriptions in API Management were always associated with a single API product scope.
    - Under certain scenarios, API publishers might want to publish an API product to the public without the requirement of subscriptions. They can deselect the Require subscription option on the Settings page of the product in the Azure portal. As a result, all APIs under the product can be accessed without an API key.
    - Azure also offers API Management support for securing APIs via OAuth 2.0, Client certificates and restricting caller IPs (allow individual IPs, CIDR block, etc.)

## Azure Key Vault
- The Key Vault aims to solve the following problems:
  - **Secrets Management**: Azure Key Vault can be used to Securely store and tightly control access to tokens, passwords, certificates, API keys, and other secrets.
    - It provides secure storage of generic secrets, such as passwords and database connection strings.
    - Key Vault APIs accept and return secret values as strings. Internally, Key Vault stores and manages secrets as sequences of octets (8-bit bytes), with a maximum size of 25k bytes each. The Key Vault service doesn't provide semantics for secrets. It merely accepts the data, encrypts it, stores it, and returns a secret identifier ("id"). The identifier can be used to retrieve the secret at a later time.
  - **Key Management**: Azure Key Vault can also be used as a Key Management solution. Azure Key Vault makes it easy to create and control the encryption keys used to encrypt your data.
  - **Certificate Management**: Azure Key Vault is also a service that lets you easily provision, manage, and deploy public and private Transport Layer Security/Secure Sockets Layer (TLS/SSL) certificates for use with Azure and your internal connected resources.
- **Why use the Key Vault?**
  - Centralize application secrets.
  - Securely store secrets and keys.
  - Monitor access and use.
  - Simplified administration of application secrets.
  - Integration with other Azure services.
- To reference secrets stored in an Azure Key Vault, you can create a secret scope backed by Azure Key Vault. Azure Key Vault-backed secrets are only supported for Azure Databricks Premium Plan.
- **Secret Scopes**: The logical grouping mechanism for secrets. All secrets belong to a scope. Scopes are identifiable by name and are unique per user's workspace.
- **Secrets**: A key-value pair that stores the secret material. Keys are identifiable secret names, and values are arbitrary data that can be interpreted as strings or bytes.
- **Secret ACLs**: Access control rules applied to secret scopes. Secret scopes and their secrets can only be accessed by users with enough permissions.
- **Secret Attributes**
  - **exp**: Expiration time on or after which the secret SHOULD NOT be retrieved. It is for informational purposes only and must be a number containing a `IntDate` value.
  - **nbf**: Not before attribute that identifies the time before which the secret data SHOULD NOT be retrieved. It is for informational purposes only and must be a number containing a `IntDate` value.
  - **enabled**: Boolean that specifies whether the secret data can be retrieved. The enabled attribute is used in conjunction with `nbf` and `exp` when an operation occurs between `nbf` and `exp`, it will only be permitted if enabled is set to true. Operations outside the nbf and exp window are automatically disallowed, except in particular situations.
  - **created**: Read only value that indicates when this version of the secret was created. This value is null for secrets created prior to the addition of this attribute. Its value must be a number containing an IntDate value.
  - **updated**: Read only value that indicates when this version of the secret was updated. This value is null for secrets that were last updated prior to the addition of this attribute. Its value must be a number containing an IntDate value.

## ADF Data Migration for Landstar Investigation
- **Linked Service**: Defines the connection to the data source.
  - For example, an Azure Storage linked service links a storage account to the data factory. An Azure Blob dataset represents the blob container and the folder within that Azure Storage account that contains the input blobs to be processed.
  - Azure Key Vault, Azure SQL Database, Azure Databricks, Azure Data Lake Storage, SQL server, etc. are all Linked services.
  - [Example Linked Service Properties JSON ](https://dev.azure.com/landstarvsts/_git/BCORetention?path=%2FlinkedService%2FSqlServerRetentionDB.json&version=GBmaster)
- **Dataset**: Identifies data within different data stores, such as tables, files, folders, and documents. It represents the structure of the data within linked data stores. Essentially, it is a named view of data that simply points or references the data you want to use in your activities as inputs and outputs.
  - **Before you create a dataset** you must create a **linked service** to link yourdata store to the data factory.

### Integration Runtime
The Integration Runtime (IR) is the compute infrastructure used by Azure Data Factory to provide the following data integration capabilities across different network environments:
- Data Flow: Execute a Data Flow in managed Azure compute environment.
  - Mapping data flows are visually designed data transformations in Azure Data Factory. Data flows allow data engineers to develop data transformation logic without writing code. The resulting data flows are executed as activities within Azure Data Factory pipelines that use scaled-out Apache Spark clusters.
- Data Movement: Copy data cross data stores in public network and data stores in the private network. Provides support for built-in connectors, format conversion, column mapping, and scalable data transfer.
- Activity Dispatch:  Dispatch and monitor transformation activities.
- SSIS Package Execution: Natively execute SQL Server Integration Services (SSIS) packages in a managed Azure compute environment.
- [Example Self-Hosted Integration Runtime (referenced from Linked Service) JSON](https://dev.azure.com/landstarvsts/_git/BCORetention?path=%2FintegrationRuntime%2FLSTR-integrationRuntime.json)

#### Integration Runtime Types
- Azure
  - Azure IR Network Environment: Azure Integration Runtime supports connecting to data stores and computes services with public accessible endpoints. Enabling Managed Virtual Network, Azure Integration Runtime supports connecting to data stores using private link service in private network environment.
    - Azure Integration runtime has properties related to Data Flow runtime, which defines the underlying compute infrastructure that would be used to run the data flows on.
  - Public Network: Data Flow, Data movement, Activity dispatch.
  - Private Network: Data Flow, Data movement, Activity dispatch.
- Self-hosted
  - Self-hosted IR Network Environment: If you want to perform data integration securely in a private network environment, which doesn't have a direct line-of-sight from the public cloud environment, you can install a self-hosted IR on premises environment behind your corporate firewall, or inside a virtual private network. The self-hosted integration runtime only makes outbound HTTP-based connections to open internet.
  - Use self-hosted integration runtime to support data stores that requires bring-your-own driver such as SAP Hana, MySQL, etc.
  - Public Network: Data movement, Activity dispatch.
  - Private Network: Data movement, Activity dispatch.
- Azure-SSIS
  - Azure-SSIS IR Network Environment: Azure-SSIS IR can be provisioned in either public network or private network. On-premises data access is supported by joining Azure-SSIS IR to a Virtual Network that is connected to your on-premises network.
  - Public Network: SSIS package execution.
  - Private Network: SSIS package execution.

##### Relationship Between Factory Location and IR Location
When customer creates a data factory instance, they need to specify the location for the data factory. The Data Factory location is where the metadata of the data factory is stored and where the triggering of the pipeline is initiated from. Metadata for the factory is only stored in the region of customer’s choice and will not be stored in other regions.

The IR Location defines the location of its back-end compute, and essentially the location where the data movement, activity dispatching, and SSIS package execution are performed. The IR location can be different from the location of the data factory it belongs to.

###### Location by Runtime Type
- Azure: You can set a certain location of an Azure IR, in which case the activity execution or dispatch will happen in that specific region.
- Self-hosted: Logically registered to the Data Factory and the compute used to support its functionalities is provided by you. Therefore there is no explicit location property for self-hosted IR. When used to perform data movement, the self-hosted IR extracts data from the source and writes into the destination.
- Azure-SSIS: Selecting the right location for your Azure-SSIS IR is essential to achieve high performance in your extract-transform-load (ETL) workflows.
  - The location of your Azure-SSIS IR does not need to be the same as the location of your data factory, but it should be the same as the location of your own Azure SQL Database or SQL Managed Instance where SSISDB.
  - If you do not have an existing SQL Database or SQL Managed Instance, but you have on-premises data sources/destinations, you should create a new Azure SQL Database or SQL Managed Instance in the same location of a virtual network connected to your on-premises network.
  - If the location of your existing Azure SQL Database or SQL Managed Instance is not the same as the location of a virtual network connected to your on-premises network, first create your Azure-SSIS IR using an existing Azure SQL Database or SQL Managed Instance and joining another virtual network in the same location, and then configure a virtual network to virtual network connection between different locations.

### Activities
The activities in a pipeline define actions to perform on your data. Data Factory has three groupings of activities: **data movement activities**, **data transformation activities**, and **control activities.** An activity can take zero or more input datasets and produce one or more output datasets.
- **Execution Activities** include data movement and data transformation activities.
- **Control Activities** are the control activities such as `Append Variable`, `If Condition`, `Lookup`, etc.
- **Activity Policy**: Policies affect the run-time behavior of an activity, giving configurability options. Activity Policies are only available for execution activities.

#### Copy Activity
- Copy Activity in Data Factory copies data from a source data store to a sink data store. This is defined as a **data movement activity**.
- Requires source and sink linked services to define the direction of data flow. The following logic is used to determine which integration runtime instance is used to perform the copy:
  - Copying between two cloud data sources: when both source and sink linked services are using Azure IR, ADF uses the regional Azure IR if you specified, or auto determine a location of Azure IR if you choose the auto resolve IR (default) option.
  - Copying between a cloud data source and a data source in private network: if either source or sink linked service points to a self-hosted IR, the copy activity is executed on that self-hosted Integration Runtime.
  - Copying between two data sources in private network: both the source and sink Linked Service must point to the same instance of integration runtime, and that integration runtime is used to execute the copy Activity.
- [Example Copy Activity Data Warehouse JSON](https://dev.azure.com/landstarvsts/_git/BCORetention?path=%2Fpipeline%2FBCO_Data_Ingest_Full_Load_DWH.json&version=GBmaster)
  - [Stored Procedure mentioned in Copy Activity JSON](https://dev.azure.com/landstarvsts/_git/BCORetention?path=%2FRetentionDB%2FRetentionDB%2Fdbo%2FStored%20Procedures%2FUSP_UPDATE_BCO_CONTROL.sql&version=GBmaster)

#### Lookup Activity
- Lookup Activity can be used to read or look up a record/table name/value from any external source. This output can further be referenced by succeeding activities. This is defined as a **control flow activity**.
- The Lookup (and GetMetadata) activity is executed on the integration runtime associated to the data store linked service.

#### For Each Activity
- Defines a repeating control flow in your pipeline. This activity is used to iterate over a collection and executes specified activities in a loop. The loop implementation of this activity is similar to the Foreach looping structure in programming languages. This is defined as a **control flow activity**.

#### If Condition Activity
- The If Condition can be used to branch based on condition that evaluates to true or false. The If Condition activity provides the same functionality that an if statement provides in programming languages. It evaluates a set of activities when the condition evaluates to true and another set of activities when the condition evaluates to false. This is defined as a **control flow activity**.

#### Data Flow Activity
- Used to transform and move data via mapping data flows. This is defined as a **data transformation activity**.
- Data Flow activities are executed on the Azure integration runtime associated to it. The Spark compute utilized by Data Flows are determined by the data flow properties in your Azure Integration Runtime and are fully managed by ADF.

### Pipeline
A pipeline is a logical grouping of activities that together perform a task. For example, a pipeline could contain a set of activities that ingest and clean log data, and then kick off a mapping data flow to analyze the log data. The pipeline allows you to manage the activities as a set instead of each one individually. You deploy and schedule the pipeline instead of the activities independently.

###### ADF Resources
- [ADF Console](https://docs.microsoft.com/en-us/azure/data-factory/control-flow-execute-data-flow-activity)
- [Microsoft Documentation for connecting to SQL Server](https://docs.microsoft.com/en-us/azure/data-factory/connector-sql-server)
- [Data Flow Activity](https://docs.microsoft.com/en-us/azure/data-factory/control-flow-execute-data-flow-activity)

### Resouces for Comparisons
- [Microsoft Azure to AWS Comparisons (Best Resource)](https://docs.microsoft.com/en-us/azure/architecture/aws-professional/services)
- [Comparison's from NetApp (Limited Examples)](https://cloud.netapp.com/blog/aws-vs-azure-cloud-storage-comparison#:~:text=Azure%20Cloud%3A%20Object%20Storage&text=AWS%20object%20storage%20comes%20in,storage%20services%20for%20unstructured%20data.)
