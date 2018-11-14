#!/bin/sh
json=$(curl -s https://api.github.com/repos/mozilla/geckodriver/releases/latest)
os=$(uname -s)
arch=$(uname -m)
if [ $os = "Linux" ] ; then
    case "$arch" in
        i386 | i486 | i786 | x86)
            url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux32"))')
            ;;        
        x86_64 | x86-64 | x64 | amd64)
            url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("linux64"))')
            ;;
        xscale | arm | armv61 | armv71 | armv81 | aarch64)
            url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("arm7hf"))')
            ;;
        *)
            echo Architecture not supported: $arch
            exit 1
            ;;
    esac
elif [ $os = "Darwin" ] ; then
    url=$(echo "$json" | jq -r '.assets[].browser_download_url | select(contains("macos"))')
fi

if [ -z $url ] ; then
    echo OS not supported: $os
    exit 1
fi

echo $url

curl -s -L "$url" | tar -xz
chmod +x geckodriver
mv geckodriver /usr/bin
