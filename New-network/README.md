We concatenated randomly selected traces from the collected real network traces in WiFi and 4G scenarios provided by PowerInfo.We only considered original traces where the average throughput is less than 4 Mbps and the minimum throughput is above 0.2Mbps.(ii) We leveraged the methods from Pensieve [10] to create a synthetic dataset.We design a dataset to cover a relatively broad set of network conditions, with average throughputs of 0.2 – 4 Mbps.
As shown in Table 2, all of the network traces are divided into three categories: strong network, medium network, and weak network according to the average throughput. Finally, three kinds of network traces are randomly mixed to generate oscillating network traces. Each network trace is a text file containing multiple lines.Each line contains two floating-point numbers: the timestamp in seconds and the measured throughput in kbps. The time interval between each network throughput sample is 0.5 secs.

Table 2: Three categories of network traces

	Category 		Range of average throughput
Strong Network 			[2.0, 4.0] (Mbps)
Medium Network 			[1.0, 2.0] (Mbps)
Weak Network 			[0.2, 1.0] (Mbps)
