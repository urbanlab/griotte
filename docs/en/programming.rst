Programming scenarios manually
******************************

Overview
========

When you create a scenario using the web interface, Blockly generates a Python
program under the hood. If you are a bit experienced, or want more freedom than you can get from the web interface, you can write those programs manually

General structure
=================

Griotte python programs are embedded in the following simple structure :

.. code-block:: python

  def run():
    # import statements ...

    while True:
      # program statements ...

  if __name__ == "__main__":
    run()

For instance, a simple "check sensor / play video" scenario could be written as :

.. code-block:: python

  def run():
    from griotte.scenario.multimedia import play_video
    from griotte.scenario.digital import wait_edge, set_profile

    set_profile('io0', { name: 'Maxbotik EZ-1', 'direction': 'input', 'pulling': 'up' })

    while True:
      if wait_edge('io0', 'falling'):
        play_video('some_funny_cat_video.m4v', sync=True)

  if __name__ == "__main__":
    run()

The version above is the generated version. Let's add comments to see what happens :

.. code-block:: python

  # The run() function is the main function called by the scenario
  def run():
    # Let's import the function required to play a video
    # Blockly generator is clever and will try to limit what's imported
    # as much as possible
    from griotte.scenario.multimedia import play_video
    # Let's import the functions we need to deal with the digital sensors
    from griotte.scenario.digital import wait_edge, set_profile

    # Set the profile for the port `io0`
    # By default, ports are `input` with a pull up enabled. So this call is not
    # strictly necessary but Blockly adds it anyway.
    # It's best to always have one so you're protected against a change in the
    # defaults.
    set_profile('io0', { name: 'Maxbotik EZ-1', 'direction': 'input', 'pulling': 'up' })

    # Loop forever
    while True:
      # Wait for the value of the port `io0` to go grom HIGH to LOW
      # This call is blocking, and since Griotte uses BCM interrupts in the
      # backoffice it will not eat the CPU like crazy
      if wait_edge('io0', 'falling'):
        # Ok, we got a `falling` transition, let's play that funny cat video
        # You do not need to specify the full path for the video : Griotte
        # handles this for you and will look in the storage, in the `video/`
        # directory.
        play_video('some_funny_cat_video.m4v', sync=True)

  # If someone runs us as a program, let's hit run()
  if __name__ == "__main__":
    run()

This code blocks until for the sensor to transition from `high` to `low`, and
then plays the cat video. Quite simple !

API
===

There are a bunch of functions you can use to program manually. They are divided
in 3 categories :

* :mod:`griotte.scenario.analog` : Analog functions (read analog value, set
  sensor profile, setup a sampling loop, ...)
* :mod:`griotte.scenario.digital` : Digital functions (read or set digital port, set sensor profile,
  wait for edge, etc ...)
* :mod:`griotte.scenario.nfc` : RFIC functions (read current tag, wait for a tag, ...)
* :mod:`griotte.scenario.multimedia` : Multimedia functions (play video, set
  sound volume, display images ...)

Debugging
=========

All griotte "binaries" support the `--logging` Tornado flag, e.g. :

  griotte/bin/server --logging=DEBUG

