# Error Policy

The Error Policy of `ospyata` is chosen to display why the `Exception` handling is left for the end user.

## Reason 1: Control

The `ospyata` library is written for `Infata`'s `Osmata`, a reflection of the Python implementation of the Osmata Project for the `Infata`. The goal of the `Infata Project` is division of control to several layers.

As per the reflection, the libraries that are part of the [`Infata Project`](https://infata.gitlab.io) will NOT handle errors which does NOT cause an issue if unhandled by the library but can be caused if the application does not handle it. This is so because such errors can be controled by the application `easily` and can cause `control` over the `application` which is not the role of a library.

## Reason 2: Complexity

`ospyata` aims to be a minimal library that can exist on its own. This also means to reduce the number of dependencies as much as possible.

Error handling by `ospyata` can cause increase in the complexity of the library. Especially when new versions are released. Also, `ospyata` doesn't raise too many `Exception`s to put a burden on the developer using this library.

## Reason 3: Beginner friendly

Apart ffrom all the above reasons, `ospyata` aims to be friendly for beginners to read and understand. `ospyata` projects aims to be helpful to beginners and professionals, and welcome contributions from both sides of the spectrum.