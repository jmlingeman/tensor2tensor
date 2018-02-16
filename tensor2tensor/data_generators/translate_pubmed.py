from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import tarfile
from shutil import copyfile

# Dependency imports

from tensor2tensor.data_generators import generator_utils
from tensor2tensor.data_generators import problem
from tensor2tensor.data_generators import text_encoder
from tensor2tensor.data_generators import translate
from tensor2tensor.utils import registry

import tensorflow as tf

FLAGS = tf.flags.FLAGS

# End-of-sentence marker.
EOS = text_encoder.EOS_ID


@registry.register_problem
class TranslatePubmed(translate.TranslateProblem):

  def __init__(self, was_reversed=False, was_copy=False):
    super(TranslatePubmed, self).__init__(was_reversed, was_copy)
    #self.root_dir = '/data/nfs/scratch1/lingeman'
    self.root_dir = '/home/lingeman/pubmed_ident/debug_data/'
    self.data_file = "pubmed_cleaned.txt"
    self.tag_file = "pubmed_mesh.txt"
    self.vocabulary_file = "pubmed_top10k.txt"
    self.vocab_size = 10000


  @property
  def targeted_vocab_size(self):
    return self.vocab_size
    # return 2**15  # 8192

  @property
  def vocab_name(self):
    return 'vocab.pubmed'

  def generator(self, data_dir, tmp_dir, train):
    tag = "train" if train else "dev"
    source_path = self.root_dir

    vocab_file = "{}/{}".format(self.root_dir, self.vocabulary_file)
    symbolizer_vocab = text_encoder.TokenTextEncoder(vocab_file, replace_oov='<UNK>')

    return translate.token_generator(source_path + self.data_file, source_path + self.tag_file,
                                     symbolizer_vocab, EOS)

  def feature_encoders(self, data_dir):

    vocab_filename = os.path.join(self.root_dir, self.vocabulary_file)
    token = text_encoder.TokenTextEncoder(vocab_filename, replace_oov='<UNK>')
    return {
      "inputs": token,
      "targets": token,
    }

  @property
  def input_space_id(self):
    return problem.SpaceID.EN_TOK

  @property
  def target_space_id(self):
    return problem.SpaceID.DE_TOK

  @property
  def use_subword_tokenizer(self):
    return False


