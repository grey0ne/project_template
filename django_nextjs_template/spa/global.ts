import { routing } from '@/i18n/routing';
import { formats } from '@/i18n/request';
import projectMessages from '@/messages/en.json';
import nextUtilsMessages from '@/next_utils/messages/en.json';

type messages = typeof projectMessages & typeof nextUtilsMessages;

declare module 'next-intl' {
    interface AppConfig {
        Locale: (typeof routing.locales)[number];
        Messages: messages;
        Formats: typeof formats;
    }
}