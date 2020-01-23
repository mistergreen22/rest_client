                                Bug reports
1. Post request doesn't validate negative value of aliases
    <br />Steps to Reproduce: 
    <br />1) Send POST request to a server with negative value of alias(-1 for example)
    <br />Expected Result: "Queue must be from 0 to 10000" message and 400 status code.
    <br />Actual Result: 201 status code is shown. 

2. Get request doesn't validate negative value of aliases
    <br />Steps to Reproduce: 
    <br />1) Send GET request to a server with negative value of alias(-1 for example) to an empty queue
    <br />Expected Result: 'Queue must be from 0 to 10000' message and 400 status code.
    <br />Actual Result: 'no messages' -message is shown. 
   
3. Delete request doesn't validate negative value of aliases
    <br />Steps to Reproduce: 
    <br />1) Send Delete request to a server with negative value of alias(-1 for example) to an empty queue
    <br />Expected Result: 'Queue must be from 0 to 10000' message and 400 status code.
    <br />Actual Result: 'no messages' -message is shown. 
    
4. Put request doesn't update oldest messages
    <br />Steps to Reproduce: 
    <br />1) Send Post request to a server with some message
    <br />2) Send Put request to a server with other
    <br />3) Send Get request to a server for get updated message
    <br />Expected Result: Updated message is shown
    <br />Actual Result: The old one message is shown
    
5. Put request doesn't work properly if trying to update message in empty queue
    <br />Steps to Reproduce: 
    <br />1) Send Put request to a server to an empty queue
    <br />Expected Result: 404 status code is shown
    <br />Actual Result: 500 status code is shown
    
6. Put request doesn't work properly if trying to update with empty message 
    <br />Steps to Reproduce: 
    <br />1) Send Post request to a server 
    <br />2) Send Put request to a server with empty message
    <br />Expected Result: 'message is empty' message is shown
    <br />Actual Result: 500 status code is shown
    
7. Put request doesn't validate negative value of aliases
    <br />Steps to Reproduce: 
    <br />1) Send Put request to a server with negative value of alias(-1 for example) to an empty queue
    <br />Expected Result: 'Queue must be from 0 to 10000' message and 400 status code.
    <br />Actual Result: 500 status code is shown. 

8. Put request doesn't validate alias value over the limit
    <br />Steps to Reproduce: 
    <br />1) Send Put request to a server with alias value bigger than limit(10001 for example) to an empty queue
    <br />Expected Result: 'Queue must be from 0 to 10000' message and 400 status code.
    <br />Actual Result: 500 status code is shown. 
    
