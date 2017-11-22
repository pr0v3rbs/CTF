# Bad (300 Points)

When connected to the server, I could get the binary which was encrypted with base64.
I needed to patch the binary to prevent the buffer overflow bug by fixing length.
And then, I sent the patched binary to the server.