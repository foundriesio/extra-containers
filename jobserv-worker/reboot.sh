#!/bin/sh -e

sync

echo s > /sysrq
sleep 1
echo b > /sysrq
