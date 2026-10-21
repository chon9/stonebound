# Stonebound uses Kivy's event/config/storage primitives through KaTrain,
# without its GUI widgets or media providers. Keep those out of the desktop bundle.
hiddenimports = ['kivy._event', 'kivy.properties', 'kivy._clock', 'kivy._metrics',
                 'kivy.utils', 'kivy.config', 'kivy.storage.jsonstore',
                 'kivy.weakmethod', 'kivy.weakproxy', 'kivy.context', 'kivy.compat',
                 'kivy.clock', 'kivy.metrics', 'kivy.event']
excludedimports = ['kivy.uix', 'kivy.core.window', 'kivy.core.audio', 'kivy.core.video',
                   'kivy.core.image', 'kivy.core.camera', 'kivy.core.text', 'kivy.input']
