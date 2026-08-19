ObjC.import('Cocoa');

ObjC.registerSubclass({
  name: 'DeepSeekAnswerTextView',
  superclass: 'NSTextView',
  methods: {
    'cancelOperation:': {
      types: ['v', ['@', ':', '@']],
      implementation: function(self, _cmd, _sender) {
        self.window.close();
      }
    }
  }
});

ObjC.registerSubclass({
  name: 'DeepSeekAnswerWindowDelegate',
  methods: {
    'windowWillClose:': {
      types: ['v', ['@', ':', '@']],
      implementation: function() {
        $.NSApp.stopModal();
      }
    },
    'windowDidResignKey:': {
      types: ['v', ['@', ':', '@']],
      implementation: function() {
        $.NSApp.stopModal();
      }
    }
  }
});

function readAnswer(answerPath) {
  const data = $.NSFileManager.defaultManager.contentsAtPath($(answerPath));
  const text = $.NSString.alloc.initWithDataEncoding(data, $.NSUTF8StringEncoding);
  return text || $('');
}

function screenForAnswer() {
  const mouse = $.NSEvent.mouseLocation;
  const screens = $.NSScreen.screens;
  for (let index = 0; index < screens.count; index += 1) {
    const screen = screens.objectAtIndex(index);
    if ($.NSPointInRect(mouse, screen.frame)) return screen;
  }
  return $.NSScreen.mainScreen;
}

function run(argv) {
  if (!argv.length) return;

  const application = $.NSApplication.sharedApplication;
  application.setActivationPolicy($.NSApplicationActivationPolicyAccessory);

  const panelSize = $.NSMakeSize(700, 440);
  const panel = $.NSPanel.alloc.initWithContentRectStyleMaskBackingDefer(
    $.NSMakeRect(0, 0, panelSize.width, panelSize.height),
    $.NSWindowStyleMaskTitled |
      $.NSWindowStyleMaskClosable |
      $.NSWindowStyleMaskResizable |
      $.NSWindowStyleMaskUtilityWindow,
    $.NSBackingStoreBuffered,
    false
  );
  panel.setTitle($('DeepSeek'));
  panel.setFloatingPanel(true);
  panel.setHidesOnDeactivate(true);
  panel.setMinSize($.NSMakeSize(420, 240));
  panel.setContentMinSize($.NSMakeSize(420, 240));

  const screen = screenForAnswer();
  const visibleFrame = screen.visibleFrame;
  panel.setFrameOrigin($.NSMakePoint(
    visibleFrame.origin.x + (visibleFrame.size.width - panelSize.width) / 2,
    visibleFrame.origin.y + (visibleFrame.size.height - panelSize.height) / 2
  ));

  const scrollView = $.NSScrollView.alloc.initWithFrame(panel.contentView.bounds);
  scrollView.setAutoresizingMask($.NSViewWidthSizable | $.NSViewHeightSizable);
  scrollView.setHasVerticalScroller(true);
  scrollView.setAutohidesScrollers(true);
  scrollView.setBorderType($.NSNoBorder);

  const textView = $.DeepSeekAnswerTextView.alloc.initWithFrame(panel.contentView.bounds);
  textView.setEditable(false);
  textView.setSelectable(true);
  textView.setRichText(false);
  textView.setImportsGraphics(false);
  textView.setUsesFindBar(true);
  textView.setUsesFindPanel(true);
  textView.setFont($.NSFont.systemFontOfSize(16));
  textView.setTextContainerInset($.NSMakeSize(18, 18));
  textView.setHorizontallyResizable(false);
  textView.setVerticallyResizable(true);
  textView.textContainer.setWidthTracksTextView(true);
  textView.setString(readAnswer(argv[0]));
  scrollView.setDocumentView(textView);
  panel.contentView.addSubview(scrollView);

  const delegate = $.DeepSeekAnswerWindowDelegate.alloc.init;
  panel.setDelegate(delegate);
  application.activateIgnoringOtherApps(true);
  panel.makeKeyAndOrderFront(null);
  panel.makeFirstResponder(textView);
  application.runModalForWindow(panel);
}
