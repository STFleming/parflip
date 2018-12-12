# parflip 0.0.1
A parallel in-hardware FPGA configuration memory fault injection framework that uses multiple Zynq-based Zedboards. 

## Generated datasets
K-means clustering HLS application.

## Setup

```bash
git clone --recursive git@github.com:STFleming/parflip.git
```

On the management machine install `dnsmasq` located in `Networking/dnsmasq` using the instructions found [here](http://thekelleys.org.uk/dnsmasq/doc.html). 

Use a network switch to connect your management machine to each Zedboard in your cluster. On each Zedboard setup an Ubuntu SDCard image using the instructions [here](https://xilinx-wiki.atlassian.net/wiki/spaces/A/pages/18841732/Ubuntu+on+Zynq).

On your management machine edit the `dnsmasq` configuration file `/etc/dnsmasq.conf` so that each Zedboard in your system has a unique name from `soc0 .. socN` where there are N+1 Zedboard in the cluster.

```
# Always give the host with Ethernet address 11:22:33:44:55:66
# the name fred and IP address 192.168.0.60 and lease time 45 minutes
#dhcp-host=11:22:33:44:55:66,fred,192.168.0.60,45m
dhcp-host=<MAC address of soc0>,soc0,192.168.0.50,infinite
dhcp-host=<MAC address of soc1>,soc1,192.168.0.51,infinite
...
dhcp-host=<MAC address of socN>,socN,192.168.0.XX,infinite
``` 

On each of the Zedboard make sure you can ssh into them and setup ssh key-based authetification with the management machine, instructions can be found [here](https://www.digitalocean.com/community/tutorials/how-to-set-up-ssh-keys--2).

Run the System setup script using the following:
```
python SystemSetup/ProvisionInjectionCode.py --number <number of Zedboards in the cluster>
```

For a simple quick power management setup connect an ATX power supply to each Zedboard in the cluster and pins 10 and 9 to pins 4 and GND of an Arduino respectively. Then use the arduino sketch in `PowerManagement/ArduinoSketches/ATX_PowerController/` to program the Arduino.

### Running an experiment
 
To construct a bitstream please follow the instructions [here](). The output should be an essential bits file, `cut.ebd` and a `cut.bin` configuration bitstream. The first step to setting up a project is to construct the linear addresses that are accepted by the SEM IP Core.

```bash
 python ExperimentManagement/generateLinearAddresses.py --input cut.ebd --output cut.la 
```

The next step is to take the file of linear addresses and chunk it up, where N is the number of chunks to produce:

```bash
 python ExperimentManagement/createChunks.py --la cut.la -- chunks N
```

We are now ready to start the experiment, where N is the number of SoCs in the experiment setup:

```bash
 python ExperimentManagement/evaluateChunks.py --number N --bit cut.bin
```
