from esp_writer.dialogues import *


def get_greeting(menu_index, menu_name, npc_id, next_id, **kwargs):
    topic = Topic('Greeting 0', 'greetings')
    info = Info(None, menu_name +' Menu', nnam=next_id, actor=npc_id)
    sub_menu = kwargs.get('submenu', [])
    info.result_text = 'set ' + 'VZ_CraftMenu_glob' + ' to ' + str(menu_index)+ '\r\n'
    for index, submenu in enumerate(sub_menu):
        if submenu is 'None':
            continue
        info.result_text += 'addtopic \"--' + submenu + '\"\r\n'

    recipes = kwargs.get('recipes', [])
    for re in recipes:
        info.result_text += 'addtopic \"-' + re['Result name'] + '\"\r\n'
    topic.add_info(info)
    return topic


def get_topic_for_submenu(menu_index, submenu, sub_index, submenu_glob):
    topic = Topic('--'+submenu)
    info_submenu = Info(get_info_id(), submenu)
    info_submenu.result_text = 'set '+submenu_glob+' to '+str(sub_index)
    info_submenu.conditions.append(Condition('global', 'VZ_CraftSubMenu_glob', '!=', sub_index))
    info_submenu.conditions.append(Condition('global', 'VZ_CraftMenu_glob', '=', menu_index))
    info_back = Info(get_info_id(), 'Back')
    info_back.conditions.append(Condition('global', 'VZ_CraftSubMenu_glob', '=', sub_index))
    info_back.conditions.append(Condition('global', 'VZ_CraftMenu_glob', '=', menu_index))
    info_back.result_text = 'set ' + submenu_glob + ' to ' + str(0)
    topic.add_info(info_submenu)
    topic.add_info(info_back)
    return topic


class CraftItems:
    def __init__(self, name, id, num):
        self.name = name
        self.id = id
        if num is '':
            self.num = 1
        else:
            self.num = int(num)


class Recipe:
    def __init__(self, items_in, items_out, menu_index, submenu_index, **kwargs):
        self.items_in = items_in
        self.items_out = items_out
        self.menu = menu_index
        self.submenu = submenu_index
        self.desc = kwargs.get('description', '')
        self.sound = kwargs.get('sound', None)
        self.energy = kwargs.get('energy', 10)

    def get_topic(self):
        topic = Topic('-' + self.items_out.name, 'regular')

        info_back = Info(get_info_id(), 'back')
        info_back.conditions.append(Condition('function', 'Choice', '=', 2))

        info_craft = Info(get_info_id(), 'Crafting ' + self.items_out.name)
        info_craft.conditions.append(Condition('function', 'Choice', '=', 1))
        for item in self.items_in:
            info_craft.conditions.append(Condition('item', item.id, '>=', int(item.num)))
            info_craft.result_text += 'Player->removeitem ' + '\"' + item.id + '\" ' + str(item.num)

        info_craft.result_text += '\r\nPlayer->additem ' + '\"' + self.items_out.id + '\" ' + str(self.items_out.num)+'\r\n'
        if self.sound is not None:
            info_craft.result_text += 'playsound \"'+self.sound+'\"\r\n'
        info_craft.result_text += 'set VZ_craft_energy_glob to VZ_craft_energy_glob - ('+str(self.energy)+'* VZ_craft_energy_mult_glob )\r\n'
        info_craft.result_text += 'MessageBox \"Energy left: \"\r\n'
        info_craft.result_text += 'Player->RemoveItem gold_001 VZ_craft_gold_final_glob\r\n'

        info_no_money = Info(get_info_id(), 'Come back when you have enough money ^pcname.')
        info_no_money.conditions.append(Condition('function', 'Choice', '=', 1))
        info_no_money.conditions.append(Condition('global', 'VZ_pc_has_money_glob', '=', 0))

        info_miss = Info(get_info_id(), 'Missing components')
        info_miss.conditions.append(Condition('function', 'Choice', '=', 1))

        info_desc = Info(get_info_id(), self.desc+'\r\nCraft level:    Your level:     Energy left: ^VZ_craft_energy_glob \r\nNeeded components:')
        info_desc.conditions.append(Condition('global', 'VZ_CraftMenu_glob', '=', self.menu))
        info_desc.conditions.append(Condition('global', 'VZ_CraftSubMenu_glob', '=', self.submenu))
        info_desc.result_text += 'set VZ_craft_gold_base_glob to 10 \r\n'
        info_desc.result_text += 'startscript VZ_craft_gold_script\r\n'
        for item in self.items_in:
            info_desc.result_text += 'MessageBox \"-' + item.name + ' ' + str(item.num) + '\"\r\n'
        # info_desc.result_text += '\r\nset VZ_craftbasecost_glob to 1\r\n'

        info_desc.result_text += 'set VZ_CraftLevel_glob to 1\r\n'
        # info_desc.result_text += 'startscript VZ_printneededskills_script\r\n'
        info_desc.result_text += 'startscript VZ_craftPrintChoices_script'

        topic.add_info(info_back)
        topic.add_info(info_craft)
        topic.add_info(info_no_money)
        topic.add_info(info_miss)
        topic.add_info(info_desc)
        return topic


class ReversedRecipe:
    def __init__(self, item_in, items_out, menu_index, submenu_index):
        self.item_in = item_in
        self.items_out = items_out
        self.menu = menu_index
        self.submenu = submenu_index

    def get_topic(self):
        topic = Topic('-'+self.item_in.name, 'regular')
        info_back = Info(get_info_id(), 'back')
        info_back.conditions.append(Condition('function', 'Choice', '=', 2))
        info_dism = Info(get_info_id(), 'Dismantling '+self.item_in.name)
        info_dism.conditions.append(Condition('function', 'Choice', '=', 1))
        info_dism.conditions.append(Condition('item', self.item_in.id, '>=', 1))
        info_dism.result_text = 'Player->removeitem '+'\"'+self.item_in.id+'\" '+str(1)
        for i in self.items_out:
            info_dism.result_text += '\r\nPlayer->additem '+'\"'+i[0].id+'\" '+str(i[0])

        info_miss = Info(get_info_id(), 'Missing components')
        info_miss.conditions.append(Condition('function', 'Choice', '=', 1))

        info_desc = Info(get_info_id(), 'Gives:')
        info_desc.conditions.append(Condition('global', 'VZ_CraftMenu_glob', '=', self.menu))
        info_desc.conditions.append(Condition('global', 'VZ_CraftSubMenu_glob', '=', self.submenu))
        info_desc.conditions.append(Condition('item', self.item_in.id, '>=', 1))
        for i in self.items_out:
            print i
            info_desc.result_text += 'MessageBox \"-'+i[0].name+' '+str(i[1])+'\"\r\n'
        #info_desc.result_text += '\r\nset VZ_craftbasecost_glob to 1\r\n'
        #info_desc.result_text += 'startscript VZ_printneededskills_script\r\n'
        info_desc.result_text += 'startscript VZ_craftPrintChoices_script'

        topic.add_info(info_back)
        topic.add_info(info_dism)
        topic.add_info(info_miss)
        topic.add_info(info_desc)
        print 'addtopic \"-'+self.item_in.name+'\"'
        return topic
