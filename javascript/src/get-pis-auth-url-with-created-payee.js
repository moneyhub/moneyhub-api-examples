import config from './config.js';
import { Moneyhub } from '@mft/moneyhub-api-client';
import yargs from 'yargs';
import { hideBin } from 'yargs/helpers';

const args = yargs(hideBin(process.argv)).option('state', {
  alias: 's',
  describe: 'state from original authorisation URL',
  default: 'foo',
}).option('nonce', {
  alias: 'n',
  describe: 'nonce for original authorisation URL',
  default: 'bar',
}).argv;

const main = async () => {
  const moneyhub = await Moneyhub(config);
  const payee = await moneyhub.addPayee({
    accountNumber: '12345678',
    name: 'payee-name',
    sortCode: '123456',
  });
  const url = await moneyhub.getPaymentAuthorizeUrl({
    state: args.state,
    amount: 1000,
    bankId: 'test',
    payeeRef: 'reference',
    payerRef: 'reference',
    payeeId: payee.data.id,
    nonce: args.nonce
  });
  console.log(url);
};

main();
