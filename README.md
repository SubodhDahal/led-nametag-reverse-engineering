# Nametag Reverse Engineering

Reverse-engineering a [LED nametag display](https://led-tag.sertronics.shop) to be programmed using a Linux system.

![Demo video](./demo.gif)

Made during the [MLH Local Hack Day 2018, Kiel](https://localhackday.mlh.io/lhd-2018/events/1299).

The application to program the display in the nametag was available for Windows systems only, so we reverse engineered the USB connection protocol and implemented it in a simpler way for use across different OSes(Linux, Windows and potentially MacOS).

## Usage

Example:

`python usb_reverse_eng.py "HELLO" --mode centered --lamp 1 --flash 0`

## Contributors

 - [Lars Thestorf](https://github.com/Lars-Thestorf)
 - [Subodh Dahal](https://github.com/SubodhDahal)
 - Raghava Vijayanagaram
 - Advanced LED Board-7 font by Sizenko Alexander
