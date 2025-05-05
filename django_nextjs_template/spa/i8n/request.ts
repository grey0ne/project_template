import { getRequestConfig } from 'next-intl/server';
import { hasLocale } from 'next-intl';
import { Formats } from 'next-intl';
import { routing } from './routing';
 
export default getRequestConfig(async ({requestLocale}) => {
    const requested = await requestLocale;
    const locale = hasLocale(routing.locales, requested)
        ? requested
        : routing.defaultLocale; 
    const projectMessages = await import(`../messages/${locale}.json`);
    const nextUtilsMessages = await import(`../next_utils/messages/${locale}.json`);
    return {
        locale,
        messages: {
            ...projectMessages.default,
            ...nextUtilsMessages.default
        }
    };
});

 
export const formats = {
    dateTime: {
        short: {
            day: 'numeric',
            month: 'short',
            year: 'numeric'
        }
    },
    number: {
        precise: {
        maximumFractionDigits: 5
        }
    },
    list: {
        enumeration: {
            style: 'long',
            type: 'conjunction'
        }
    }
} satisfies Formats;