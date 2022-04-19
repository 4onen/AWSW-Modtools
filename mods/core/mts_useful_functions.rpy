init -1 python:
    def mts_yes_no_prompt(string):
        ui.frame(xalign=0.5, yalign=0.5)
        ui.add("image/ui/menubg_options.png", at=popup_custom)
        ui.vbox(at=popup_custom)
        ui.null(height=30)

        ui.text(string,
                style="yesno_prompt_text",
                xcenter=0.5, ycenter=0.5)

        ui.null(height=50)
        ui.hbox(xcenter=0.5, ycenter=0.5)

        ui.textbutton("Yes",
                        clicked=[ui.returns(True), Play("audio", "se/sounds/yes.wav")],
                        hovered=[Play("audio", "se/sounds/select.ogg")],
                        style="yesnobutton")

        ui.null(width=250)

        ui.textbutton("No",
                        clicked=[ui.returns(False), Play("audio", "se/sounds/close.ogg")],
                        hovered=[Play("audio", "se/sounds/select.ogg")],
                        style="yesnobutton")
        ui.close()
        ui.close()

        return ui.interact()

    def mts_ok_prompt(string):
        ui.frame(xalign=0.5, yalign=0.5)
        ui.add("image/ui/menubg_options.png", at=popup_custom)
        ui.vbox(at=popup_custom)
        ui.null(height=30)

        ui.text(string,
                style="yesno_prompt_text",
                xcenter=0.5, ycenter=0.5)

        ui.null(height=50)
        ui.hbox(xcenter=0.5, ycenter=0.5)

        ui.textbutton("OK",
                        clicked=[ui.returns(True), Play("audio", "se/sounds/yes.wav")],
                        hovered=[Play("audio", "se/sounds/select.ogg")],
                        style="yesnobutton")

        ui.close()
        ui.close()

        return ui.interact()

    def mts_var_exists(var):
        if var in renpy.python.store_dicts["store"]:
            return True

        return False

    def mts_is_mod_installed(mod):
        for mod_name in modinfo.modlist:
            if mod_name == mod:
                return True

        return False

init -100 python:
    @renpy.pure
    def MTSSetPersistent(name, value):
        return SetField(persistent, name, value)

    @renpy.pure
    def MTSTogglePersistentBool(name):
        return ToggleField(persistent, name, True, False)

###Some transforms
transform popup_custom:
    xalign 0.5 yalign 0.5 alpha 0.0 yzoom 0.0
    easein 0.3 alpha 1.0 yzoom 1.0
    on hide:
        easeout 0.3 alpha 0.0 yzoom 0.0
