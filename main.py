import logging

from BotSrc.TGBot import TG_ART_BOT

# main {
def main():

    TG_ART_BOT.delete_webhook(drop_pending_updates=True)
    TG_ART_BOT.polling(non_stop=True, interval=0)

    pass
# main }

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()

    pass