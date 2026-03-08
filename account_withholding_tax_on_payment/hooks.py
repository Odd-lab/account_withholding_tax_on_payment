def pre_init_hook(env):
    lang_th = env.ref("base.lang_th", raise_if_not_found=False)
    if lang_th and not lang_th.active:
        lang_th.write({"active": True})
