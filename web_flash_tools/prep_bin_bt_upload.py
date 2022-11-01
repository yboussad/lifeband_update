import os
import re


bin_dir = "/home/yanis/Documents/web_flash_tools/"
firmware_dir = "/home/yanis/Documents/PlatformIO/Projects/WIFI_UPLOAD_FIRMEWARE/"



command = '"/home/yanis/.platformio/penv/bin/python" "/home/yanis/.platformio/packages/tool-esptoolpy/esptool.py" --chip esp32 --port "/dev/ttyUSB0" --baud 460800 --before default_reset --after hard_reset write_flash -z --flash_mode dio --flash_freq 80m --flash_size 4MB 0x1000 /home/yanis/.platformio/packages/framework-arduinoespressif32/tools/sdk/esp32/bin/bootloader_qio_80m.bin 0x8000 /home/yanis/Documents/PlatformIO/Projects/WIFI_UPLOAD_FIRMEWARE/.pio/build/esp32cam/partitions.bin 0xe000 /home/yanis/.platformio/packages/framework-arduinoespressif32/tools/partitions/boot_app0.bin 0x10000 .pio/build/esp32cam/firmware.bin'

offset_bins = [e.split(' ') for e in re.findall("0[xX][0-9a-fA-F]+ [\/.\w-]+?(?=\.).bin", command)]
offset_bins[-1][-1] = firmware_dir + offset_bins[-1][-1]
print(offset_bins)
[os.popen('cp {} {}/{}'.format(e[1], bin_dir,
                               'bt_ul_'+e[1].split('/')[-1])) for e in offset_bins]

offset_bins = {path.split('/')[-1][:-4]:(int(offset, 16), path.split('/')[-1]) for  offset, path in offset_bins}

print(offset_bins)
manifest = """{{  "name": "Lifeband with BT upload update",  "builds": [    {{      "chipFamily": "ESP32",      "improv": false,      "parts": [        {{ "path": "bt_ul_{0}", "offset": {1} }},        {{ "path": "bt_ul_{2}", "offset": {3} }},        {{ "path": "bt_ul_{4}", "offset": {5} }},        {{ "path": "bt_ul_{6}", "offset": {7} }}      ]    }}  ]}}""".format(offset_bins['boot_app0'][1], offset_bins['boot_app0'][0],                                                                                                                                                                                                                                                                      offset_bins['firmware'][1], offset_bins['firmware'][0],                                                                                                                                                                                                                                                offset_bins['bootloader_qio_80m'][1], offset_bins['bootloader_qio_80m'][0],                                                                                                                                                                                                                                                            offset_bins['partitions'][1], offset_bins['partitions'][0])
with open('bt_ul_manifest.json', 'w') as f:
    f.writelines(manifest)

