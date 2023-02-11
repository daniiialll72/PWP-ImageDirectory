# Important information for Deadline 2


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 2** *(see course information at [Lovelace](http://lovelace.oulu.fi))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
In this section students must design and implement the database structure (mainly the data model).

In this section you must implement:
<ul>
<li>The database table structure.</li>
<li>The data models (ORM)</li>
<li>Data models access methods (if needed)</li>
<li>Populating the database using the models you have created</li>
<ul>
</bloquote>
<strong>In this section you should aim for a high quality small implementation instead of implementing a lot of features containing bugs and lack of proper documentation.</strong>
<h3>SECTION GOALS:</h3>
<ol>
<li>Understand database basics</li>
<li>Understand how to use ORM to create database schema and populate a database</li>
<li>Setup and configure database</li>
<li>Implement database backend</li>
</ol>
</details>

---

<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 5 points)</strong>
</summary>

<bloquote>
You can get a maximum of 5 points after completing this section. More detailed evaluation is provided in the evaluation sheet in Lovelace.
</bloquote>

</details>

---

# Database design and implementation

## Database design
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Describe your database. The documentation must include:
<ul>
<li>A name and a short description of each database model. Describe in one or two sentences what the model represents.</li>
<li>An enumeration of the attributes (columns) of each model. Each attribute must include:
	<ul>
		<li>Its type and restrictions (values that can take)</li>
		<li>A short description of the attribute whenever the name is not explicit enough. E.g. If you are describing the users of a "forum", it is not necessary to explain the attributes "name", "surname" or "address" </li>because their meanings are obvious.
		<li>Characteristics of this attribute (e.g. if it is unique, if it contains default values)</li>
	</ul>
</li>
<li>Connection with other models (primary keys and foreign keys)</li>
<li>Other keys</li>
</ul>
You can use the table skeleton provided below

For this section you can use a visual tool to generate a diagram. Be sure that the digram contains all the information provided in the models. Some tools you can use include: <a href="https://www.dbdesigner.net/">https://dbdesigner.net/</a>, <a href="https://www.lucidchart.com/pages/tour/ER_diagram_tool">https://www.lucidchart.com/pages/tour/ER_diagram_tool</a>, <a href="https://dbdiffo.com/">https://dbdiffo.com/</a>

</bloquote>
</details>

In this section we will discuss about the database tools, the structure, ORM, and the data we store in each field.

### Research about the best solutions
The data that we are getting involved in this project can be separeted to two different types. 1. Image data (byte arrays) 2. Text data (user information, metadata of each image, etc)

Storing images in databases like MySQL and MongoDB can have some disadvantages. Here are a few of them:

* Increased storage overhead: Storing images directly in databases like MySQL or MongoDB can increase the storage overhead, as binary data typically takes up more space than other data types.

* Performance issues: Querying images stored in databases can be slower than querying other data types, due to the size of the data and the overhead of fetching and processing binary data.

* Limitations on file size: Databases like MySQL have limits on the maximum size of a single record, which can limit the size of the images that can be stored in the database. MongoDB, on the other hand, has a larger document size limit, but still, storing large images can impact performance and create issues with disk space.

* Complexity: Storing images in databases requires additional code and logic to handle the binary data.

* Data management: When images are stored in databases, it becomes more difficult to manage the data outside of the database, such as backing up and archiving data, or moving it to different storage locations.

As a result, we have decided to store images in a separate storage solution, which is called [MinIO](https://min.io/).

#### MINIO
[MinIO](https://min.io/) is an open-source object storage server that is designed to be highly scalable and performant. MinIO is designed to be simple to use and highly available, and it supports multi-cloud deployments.

Here are some key features of MinIO:

* Object storage: MinIO stores data as objects, which are essentially files with metadata. Objects can be any type of data, including images, videos, backups, and more.

* High performance: MinIO is optimized for high performance and is designed to handle large amounts of data with low latency.

* Scalability: MinIO is designed for horizontal scalability, meaning you can add more storage capacity by adding more servers.

* High availability: MinIO supports high availability through data replication, so you can ensure that your data is always available, even if one of the servers fails.

* Security: MinIO supports encryption and role-based access control, so you can secure your data and control who has access to it.

#### MongoDB
Regarding the three top high priority missions that our application shoul have, we selected MongoDB to store text-based data. These three high priority missions are:
1. Flexibility in storing document based data
2. High-performance in data retrieval
3. Supporting query language and data integration

(MongoDB)[https://www.mongodb.com/] is a popular NoSQL document-oriented database that provides a flexible and scalable database solution. Here are some more details about MongoDB and its features:

* Document-oriented data model: MongoDB stores data in documents, which are like JSON objects, and are stored in collections. This makes it easier to store and query complex data structures.

* Dynamic schema: MongoDB does not enforce a strict schema, which allows for more flexible and dynamic data structures. This means that you can store different types of data in the same collection, and you don't have to define the structure of your data beforehand.

* Scalability: MongoDB is designed for horizontal scalability, which means that you can easily add more servers to increase your database's capacity.

* High performance: MongoDB uses indexes to improve query performance, and it supports in-memory storage and other performance optimizations.

* Rich query language: MongoDB supports a rich query language that allows you to query data using complex conditions, perform aggregations, and more.

### Models and Table

---

:pencil2: *The table can have the following structure*

|**Name** | **Type**|**Restrictions**|**Description**|**Characteristics** | **Links**|
|:------: |:-------:|:--------------:|:-------------:|:-----------------: |:--------:|
|Name of the attribute|Attribute type|Values that the type can take|Description of the attribute|Uniquenes, default...| keys and foreign keys|
||||||| 
||||||| 
||||||| 

:pencil2: *Do not forget to include a diagram presenting the relations*

---

## Database implementation
<details>
<summary>
:computer:&nbsp;&nbsp;&nbsp;&nbsp; <strong>TODO: SOFTWARE TO DELIVER IN THIS SECTION</strong>
</summary>

<bloquote>
<strong>The code repository must contain: </strong>
<ol>
<li>The ORM models and functions</li>
<li>A <var>.sql dump</var> (or similar data structure) of a database or the <var>.db file</var> (if you are using SQlite). The provided document must contain enough information to replicate your database. You must provide a populated database in order to test your models.</li>
<li>The scripts used to generate your database (if any)</li>

<li>A README.md file containing:
	<ul>
		<li>All dependencies (external libraries) and how to install them</li>
		<li>Define database (MySQL, SQLite, MariaDB, MongoDB...) and version utilized</li>
		<li>Instructions how to setup the database framework and external libraries you might have used, or a link where it is clearly explained. </li>
		<li>Instructions on how to setup and populate the database.</li>
	</ul>
</li>
<li> If you are using python a `requirements.txt` with the dependencies</li>
</ol>

</bloquote>

</details>

---

:pencil2: *You do not need to write anything in this section, just complete the implementation.*

---

## Resources allocation 
|**Task** | **Student**|**Estimated time**|
|:------: |:----------:|:----------------:|
|||| 
|||| 
|||| 
|||| 
|||| 