cd ~
apt update
$(git clone https://github.com/intel-iot-devkit/terasic-de10-nano-kit.git)

cd /home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule

$(python3.7 -m pip install -r ./requirements.txt)


export IOTHUB_DEVICE_SECURITY_TYPE="DPS"
export IOTHUB_DEVICE_DPS_ID_SCOPE="gouthamAD"
export IOTHUB_DEVICE_DPS_DEVICE_ID="DE10NANO"
export IOTHUB_DEVICE_DPS_DEVICE_KEY="djKvllwn5EuKDEcQlPN0BHbf+m+JxLzhaKQ1lsv+5h+9B9mjutiymIVdHTb7RT9VIwgqdfCoG/u0NY+Tjjxjag=="

overlay_dir="/sys/kernel/config/device-tree/overlays/socfpga_1"
overlay_dtbo="rfs-overlay.dtbo"
overlay_rbf="Module5_Sample_HW.rbf"

if [ -d $overlay_dir ];then
    rmdir $overlay_dir
fi

$(git clone https://github.com/g00g1y5p4/FPGA2cloudPrerequisites.git)

cd "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/overlay/"

cp $overlay_dtbo /lib/firmware/
cp $overlay_rbf /lib/firmware/

mkdir $overlay_dir



#echo "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/overlay/rfs-overlay.dtbo" > $overlay_dir/path

cd "/home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/"

cp FPGA2cloudPrerequisites/main.py ./

$(python3.7 -u /home/root/terasic-de10-nano-kit/azure-de10nano-document/sensor-aggregation-reference-design-for-azure/sw/software-code/modules/RfsModule/main.py)

