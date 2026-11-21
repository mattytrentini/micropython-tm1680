# TM1680 for MicroPython

MIT-licensed I²C driver for 16×16 monochrome panels wired like the
[M5Stack CoreMatrix](https://docs.m5stack.com/en/core/CoreMatrix). It uses
MicroPython's native one-bit `framebuf.FrameBuffer` and sends each image
in one I²C transaction using a reusable 33-byte transmit buffer.

## Install

```sh
mpremote mip install github:mattytrentini/micropython-tm1680
```

On a network-connected device:

```python
import mip
mip.install("github:mattytrentini/micropython-tm1680")
```

## Draw

Provide an initialized I²C bus and power the display before construction.
On CoreMatrix, the M5IOE1 expander controls the display rail; the
[CoreMatrix application](https://github.com/mattytrentini/m5stack-core-matrix-app)
handles that setup and installs this driver automatically.

```python
from tm1680 import TM1680

display = TM1680(i2c, address=0x72, brightness=2)
display.text("HI", 0, 4, 1)
display.show()
```

`brightness(0)` blanks the display without changing the framebuffer.
Levels 1–16 set global PWM duty. `deinit()` disables the display and its
oscillator but does not switch the external power rail.

Protocol and wiring references: [TM1680 datasheet](https://datasheet.lcsc.com/datasheet/pdf/11c225efe9ad4391ba4fc8ffaab5702e.pdf?productCode=C84836)
and [M5GFX panel implementation](https://github.com/m5stack/M5GFX/blob/master/src/lgfx/v1/panel/Panel_TM1680.inl).
