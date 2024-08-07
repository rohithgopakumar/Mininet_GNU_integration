# Mininet_GNU_integration
Part of project which involves integration of gnu with mininet in order to be able to send traffic from gnu satellite block and integrate with mininet .


This has been created to document my journey integration of mininet and GNU radio.




# COURSE 
<details>
<summary>DAY 1: Sending Sin wave from host1 to host2</summary>
<br>


## Creating a GNU FlowGraph

In order to send a sine wave from GNU radio using mininet we have to follow certain steps. Firstly we have to create a GNU Flowgraph as below

![image](https://github.com/user-attachments/assets/58b0f9a3-a39e-4f6f-b837-5082cfc445bb)
This will be our reciever , let us name it tcp_recieve 


![image](https://github.com/user-attachments/assets/135074b0-914b-407f-9252-fdfe2edf4818)
This will be our transmitter, let us name it tcp_sin_send




## Running mininet

Create a simple SDN Topology with 2 switches, 2 hosts and a pox controller in mininet and run mininet. Run the Pox controller and ensure we are able to ping H1 and H2 and vice-versa.











</details>
<details>
<summary>DAY 2 : Sending an AM modulated signal from host1 to host2 </summary>
<br>
