# azure-rate-limiting
'''
Documentation for Queue-Based Load Leveling pattern implementation 

AIM: Reduce memory consumption by dequeuing records only when there is capacity to process them.

A throttled service is a service that intentionally limits the rate at which clients can access its resources or perform operations.
Throttling is typically implemented to manage the consumption of resources, prevent overload situations,ensure fair usage among all users
and protect the stability and performance of the service. When a service is throttled, clients may experience delays, timeouts, 
or rejection of requests if they exceed the allowed rate of access.

The rate limiting pattern is typically implemented in response to a service that is throttled. The rate limiting patter which is implemented 
here is called Queue-Based load leveling pattern. This pattern use a queue that acts as a buffer between a task and a service it 
invokes in order to smooth intermittent heavy loads that can cause the service to fail or the task to time out.
This can help to minimize the impact of peaks in demand on availability and responsiveness for both the task and the service.

CONTEXT AND PROBLEM 

Cloud services can face issues with performance and reliability when they're hit with sudden bursts of heavy use. 
These services might be part of the same system or provided by third-party providers like storage or caching services.
When lots of tasks use the same service at once, it's hard to predict how much demand it will face. 
Sometimes, the service gets overwhelmed by too many requests and can't respond properly.If too many requests come in at once,
the service might even crash. To avoid these problems,it's important to manage resources well and plan for scalability.

SOLUTION

The solution is to introduce a queue between the task and the service. The task and the service run asynchronously.
The task posts a message containing the data required by the service to a queue. The queue acts as a buffer, 
storing the message until it's retrieved by the service. The service retrieves the messages from the queue and processes them. 
Requests from a number of tasks, which can be generated at a highly variable rate, can be passed to the service through the same 
message queue.The queue decouples the tasks from the service, and the service can handle the messages at its own pace regardless 
of the volume of requests from concurrent tasks. Additionally, there's no delay to a task if the service isn't available at the
time it posts a message to the queue.
''' 
