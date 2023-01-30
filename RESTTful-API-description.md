# Important information for Deadline 1


:bangbang:&nbsp;&nbsp;**This chapter should be completed by Deadline 1** *(see course information at [Lovelace](http://lovelace.oulu.fi/ohjelmoitava-web/ohjelmoitava-web/))*

---
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Chapter summary</strong>
</summary>

<bloquote>
This chapter must provide a good overview of the Web API that your group is going to develop during the course, and some insight into the (imaginary) microservice architecture it will be a part of. You should not focus in implementation aspects such as database structure,  interfaces or the request/responses formats. We recommend that you look into existing APIs (see Related work below) before writing the description for your own API.

<h3>Chapter GOALS:</h3>
<ol>
<li>Understand what is an API</li>
<li>Describe the project topic API</li>
<li>Describe how the API would be used as part of a larger architecture</li>
</ol>
</bloquote>

</details>

---

<details>
<summary>
:heavy_check_mark:&nbsp;&nbsp;&nbsp;&nbsp; <strong>Chapter evaluation (max 5 points)</strong>
</summary>

<bloquote>
You can get a maximum of 5 points after completing this Chapter. More detailed evaluation is provided in the evaluation sheet in Lovelace.
</bloquote>

</details>

---

# RESTful API description
## Overview
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>

Describe the API you are going to implement. Also describe the larger imaginary architecture that would exist around that API - while you do not need to implement these other components, they will be helpful in imagining context for your API. Your API will be a component that stores, and offers an interface to, some important data in the larger ecosystem. Think about a larger system, and then take out one key piece to examine - this will be your API.

Describe the API briefly and comment what is the main functionality that it exposes. Focus in the API not in any specific application that is using this API. Take into account that in the end, a WEB API is an encapsulated functionality as well as the interface to access that functionality. Remember that your API is just one part of a larger machine. It does not need to do everything. There will be other components in the system to do those things. This course focuses on creating a small API in detail - thinking too big from the start will drown you in work later. 

A really short version of an overview for the RESTful Web API could be: 

<em>“The discussion forum Web API offers different functionalities to structure non-real-time conversations among the people of a group about topics they are interested in certain topic. Messages are grouped in Threads, that at the same time are grouped in Topics. The messages are accessible to anyone, but posts can only be created by providing credentials of a registered user [...] This API could exist as part of an online learning environment system where it is responsible for offering discussion forum features that can be included in other components of the learning environment. For example, a programming task (managed by a different component) can include its own discussion board managed by the discussion forum API[...]“</em>

</bloquote>

</details>

---

The Image Directory app API will provide the necessary functionality for administrators to manage the image database and for users to upload and tag their own images. The API will allow administrators to add images to the database, as well as search for specific images based on their tags and metadata. For users, the API will provide the ability to upload images either through direct upload or file browser. Additionally, users will be able to tag their images to make them easier to find and categorize.

---


## Main concepts and relations
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
<strong>Define</strong> the <strong>main concepts</strong> and describe the <strong>relations</strong> among them textually. Roughly, a concept is a real-world entity that is expected to be of interest to users or other services. This section will be a guideline for choosing your resources to implement in Deadline 3. Students should remember that some of the concepts might not be a resource by themselves, but just a part of it (resource property). In this section, students should not describe the RESTful resources, but identify which are the main ideas of the API. Do not forget to include the relations among the concepts.

A description of the main concepts for the Forum API could be: 

<em>"The API permits users send messages. The forum contains a list of categories and a list of users. Each category specifies a name, a description and a thread. A thread is [...]The forum may contain 0 or more categories… Each category may have 0 or more threads… Users can write and read messages to a forum thread. A user has a profile, basic information, activity information (stores, for instance, all the messages sent by a user, the messages marked as favorites). [...]The user history contains information of the last 30 messages sent by the user.[…]"</em>

Include a diagram which shows the relations among concepts.

This section is important because it outlines the concepts that you will later implement. In particular, the diagram defined here will follow you throughout the project report and you will be adding more details to it. 


</bloquote>

</details>

---

Image: The main concept of the Image Directory app API is the image. An image represents a visual representation of a real-world object or event.

User: Users are individuals who have the ability to upload and tag images in the Image Directory app. They are also able to search for images in the database.

Administrator: Administrators are responsible for managing the images in the Image Directory app. They have the ability to add images to the database and perform searches on the images.

Image Upload: This concept represents the process by which users can upload images to the Image Directory app. This can be done either through a direct upload or file browser.

Image Tagging: This concept represents the process by which users can add descriptive tags to their images to make them easier to categorize and find.

Image Search: This concept represents the process by which users and administrators can search for images in the Image Directory app. Searches can be based on the tags and metadata associated with the images.

Authentication: This concept represents the process by which users are authenticated and authorized to access the Image Directory app.

Relations:

Image - User: A User can upload and tag Images.

Image - Administrator: An Administrator can add Images to the database and perform searches on the Images.

Image Upload - User: Only a User can upload Images to the Image Directory app.

Image Tagging - User: Only a User can tag Images in the Image Directory app.

Image Search - User, Administrator: Both Users and Administrators can perform searches on the Images in the Image Directory app.

Authentication - User, Administrator: Both Users and Administrators are required to be authenticated and authorized to access the Image Directory app.

---

## API uses
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Describe at least one client and one service that could use your Web API. You must explain here what is the functionality provided by the client/service, and how it uses the Web API to implement this functionality. 
</bloquote>

</details>

---

Image Tagging Client: An image tagging client is a software application that provides users with the ability to add descriptive tags to their images. This client would use the Image Directory API to retrieve images from the database and to add tags to the images. The client would send a request to the API to retrieve the images, then display them to the user in a graphical user interface. The user would then be able to add tags to the images, which the client would then send back to the API to update the image's metadata.

Image Search Service: An image search service is a software service that provides users and administrators with the ability to search for images in the Image Directory. This service would use the Image Directory API to retrieve images from the database and to perform searches based on the tags and metadata associated with the images. The service would send a request to the API with a search query, which would return a list of images that match the query. The service would then display the images to the user or administrator.


## Related work
<details>
<summary>
:bookmark_tabs:&nbsp;&nbsp;<strong>Content that must be included in the section</strong>
</summary>

<bloquote>
Find at least one API that resembles the functionality provided by yours. Explain in detail the functionality provided by the API. Classify the API according to its type (RPC, CRUD REST, pure REST, hypermedia driven ...) justifying your selection. Provide at least one example client that uses this API.

The purpose of this task is to get more familiar with what an API is. This will be helpful in describing your own API. Therefore, it is recommended to do this section after you have decided the topic of your project but before writing your API description.
</bloquote>

</details>

---

Flickr API: The Flickr API resembles the functionality provided by the Image Directory API. The Flickr API provides developers with access to millions of photos and videos from the Flickr community. The API provides functionality for retrieving photos, uploading photos, and searching for photos.

Functionality provided by Flickr API:

Retrieving Photos: The Flickr API provides functionality for retrieving photos from the Flickr community. This functionality includes retrieving photos based on specific search criteria such as tags, user ID, and location.
Uploading Photos: The Flickr API provides functionality for uploading photos to the Flickr community. This functionality includes the ability to upload photos in multiple sizes and to specify the privacy level for the photos.
Searching for Photos: The Flickr API provides functionality for searching for photos in the Flickr community. This functionality includes searching for photos based on specific search criteria such as tags, user ID, and location.
API classification: The Flickr API is a pure REST API. This is because it uses HTTP methods such as GET, POST, and DELETE to perform operations on the API resources. The API follows the REST architectural style, which is characterized by a client-server architecture, statelessness, cacheability, and a uniform interface.

Example client: One example client that uses the Flickr API is the Flickr app for iOS. This app allows users to view their photos on the Flickr community, upload photos to the community, and search for photos. The app uses the Flickr API to perform these operations and to display the results to the user in a graphical user interface.

---


## Resources allocation
|**Task** | **Student**|**Estimated time**|
|:------: |:----------:|:----------------:|
|Backend-API|Danial Khaledi|1 month| 
|Backend-API|Mehrdad Kaheh|1 month| 
|Frontend-Client|Nazanin Nakhae|3 Weeks| 
|Frontend-Client|Sepehr Samadi|3 weeks| 
|||| 
