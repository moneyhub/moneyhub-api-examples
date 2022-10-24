import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const DEFAULT_SCOPES = 'accounts:read transactions:read:all';

const args = yargs(hideBin(process.argv))
  .option('userId', {
    alias: 'u',
    describe: 'userId to get token for',
  })
  .option('scope', {
    alias: 's',
    describe: 'scopes to request',
    default: DEFAULT_SCOPES,
  }).argv;

const main = async () => {
  const moneyhub = await Moneyhub(config);
  const url = await moneyhub.getClientCredentialTokens({
    scope: args.scope,
    sub: args.userId,
  });
  console.log(url);
};

main();
