import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const args = yargs(hideBin(process.argv))
  .option('code', {
    alias: 'c',
    describe: 'code to exchange code for tokens',
  })
  .option('nonce', {
    alias: 'n',
    describe: 'nonce from original authorisation URL',
    default: 'bar',
  })
  .option('id_token', {
    alias: 'i',
    describe: 'id_token from redirect url',
  })
  .option('state', {
    alias: 's',
    describe: 'state from original authorisation URL',
    default: 'foo',
  }).argv;

const main = async (code) => {
  const moneyhub = await Moneyhub(config);

  const tokens = await moneyhub.exchangeCodeForTokens({
    localParams: {
      state: args.state,
      nonce: args.nonce,
    },
    paramsFromCallback: {
      code: args.code,
      state: args.state,
      id_token: args.id_token
    },
  });

  console.log(tokens);
};

main();
