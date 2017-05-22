#!/usr/bin/env bash

df -h | grep root | awk '{print $5}'
