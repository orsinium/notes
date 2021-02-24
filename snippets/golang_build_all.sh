set -e

# Build a golang project for all supported systems and architectures

export NAME="project-name"
export PACKAGE="."

get_targets() {
	go tool dist list | sed -e 's|/|-|'
	echo linux-386-387
	echo linux-arm-arm5
}

get_ext() {
    if [ "$1" = "windows" ]; then
		echo ".exe"
        return 0
	fi
    echo ".bin"
}

mkdir -p dist/
targets=$(get_targets | sort)
for target in $targets
do
	export GOOS=$(echo $target | sed 's/-.*//')
	export GOARCH=$(echo $target | sed 's/.*-//')
	echo "os=$GOOS arch=$GOARCH"
	unset GO386 GOARM
	if [ "$GOARCH" = "arm5" ]; then
		export GOARCH=arm
		export GOARM=5
	fi
	if [ "$GOARCH" = "387" ]; then
		export GOARCH=386
		export GO386=387
    fi
    ext=$(get_ext $GOOS)
	go build -o dist/$NAME-$target$ext $PACKAGE
done
