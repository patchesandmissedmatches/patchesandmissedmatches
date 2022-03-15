# patchloader.py
#   PatchLoader class
#
# Jiyong Jang, 2012
#
import os
import re
import time
import mimetypes
import Methods.common as common
from html.parser import HTMLParser

class PatchLoader(object):

    def __init__(self):
        self._patch_list = []
        self._npatch = 0
        self._hashes = {}
        self._only_removed = []
        self._only_added = []
        
    def traverse(self, patch_path, typePatch):
        '''
        Traverse patch files
        '''
#         common.verbose_print('[+] traversing patch files')
        start_time = time.time()

        if os.path.isfile(patch_path):
            magic_type = common.file_type(patch_path)
#             common.verbose_print('  [-] %s: %s' % (patch_path, magic_type))
            if magic_type.startswith('text'):
                main_type, sub_type = magic_type.split('/')
                if typePatch == 'buggy':
                    self._process_buggy(patch_path)
                elif typePatch == 'patch':
                    self._process_patch(patch_path)
        elif os.path.isdir(patch_path):
            for root,dirs,files in os.walk(patch_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    magic_type = common.file_type(file_path)
#                     common.verbose_print('  [-] %s: %s' % (file_path, magic_type))
                    if magic_type.startswith('text'):
                        main_type, sub_type = magic_type.split('/')
                        if typePatch == 'buggy':
                            self._process_buggy(file_path)
                        elif typePatch == 'patch':
                            self._process_patch(file_path)
        self._npatch = len(self._patch_list)

        elapsed_time = time.time() - start_time
#         print ('[+] %d patches ... %.1fs\n' % (self._npatch, elapsed_time))
        return self._npatch

    def _process_buggy(self, patch_path):
        '''
        Normalize a patch file and build a hash list
        '''
        patch_filename = patch_path.split('/')[-1]
        patch_file = open(patch_path, 'r')
        patch_lines = patch_file.readlines()
        patch_file.close()
        magic_ext = None
        process_flag = False
        diff_file = ''
        diff_cnt = 0
        diff_buggy_lines = []
        orig_norm_lines = []
        diff_orig_lines = []
        
        removed_lines = []
        
        for line in patch_lines:
            diff_file = re.sub('\.patch$', '', patch_path)
            magic_ext = self._get_file_type(diff_file)
            if line.startswith('@@'):     
                if diff_buggy_lines:
#                     common.verbose_print('\nDiff buggy lines')
#                     common.verbose_print(diff_buggy_lines)
                    diff_norm_lines = self._normalize(''.join(diff_buggy_lines), magic_ext).split()
#                     common.verbose_print('\nBuggy norm lines')
#                     common.verbose_print(diff_norm_lines)
                    if len(diff_norm_lines) >= common.ngram_size:
#                         common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                        path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                        hash_list = self._build_hash_list(diff_norm_lines)
#                         common.verbose_print('\nHash list\n', hash_list, '\n')
                        self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_orig_lines), diff_norm_lines, hash_list))
                    else:
#                         common.verbose_print('Adjusting ngram_size')
                        common.ngram_size = len(diff_norm_lines)
#                         common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                        path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                        hash_list = self._build_hash_list(diff_norm_lines)
#                         common.verbose_print('\nHash list\n', hash_list, '\n')
                        self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_orig_lines), diff_norm_lines, hash_list))
                    del diff_buggy_lines[:]
                    del orig_norm_lines[:]
                if removed_lines:
                    removed_norm_lines = []
                    for removed in removed_lines:
                        removed_norm_lines.append(self._normalize(''.join(removed), magic_ext).split())
#                         hash1_r = common.fnv1a_hash(ngram) & (common.bloomfilter_size-1)
#                         hash2_r = common.djb2_hash(ngram) & (common.bloomfilter_size-1)
#                         hash3_r = common.sdbm_hash(ngram) & (common.bloomfilter_size-1)
#                         hash_list_removed = [hash1_r, hash2_r, hash3_r]
                        self._only_removed.append(removed_norm_lines)
                        
                    del removed_lines[:]
                diff_cnt += 1

            elif line.startswith('-'):
                diff_buggy_lines.append(line[1:])
                diff_orig_lines.append('<font color=\"#AA0000\">')
                diff_orig_lines.append(line.replace('<','&lt;').replace('>','&gt;'))
                diff_orig_lines.append('</font>')
                removed_lines.append(line[1:])

            elif line.startswith(' '):
                diff_buggy_lines.append(line[1:])
                diff_orig_lines.append(line.replace('<','&lt;').replace('>','&gt;'))

#         common.verbose_print('\nDiff buggy lines')
#         common.verbose_print(diff_buggy_lines)
        if diff_buggy_lines:
            buggy_norm_lines = self._normalize(''.join(diff_buggy_lines), magic_ext).split()
#             common.verbose_print('\nBuggy norm lines')
#             common.verbose_print(buggy_norm_lines)
            if len(buggy_norm_lines) >= common.ngram_size:
#                 common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                hash_list = self._build_hash_list(buggy_norm_lines)
#                 common.verbose_print('\nHash list\n', hash_list, '\n')
                self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_buggy_lines), buggy_norm_lines, hash_list))
            else:
#                 print('Adjusting ngram_size')
                path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                common.ngram_size = len(buggy_norm_lines)
                hash_list = self._build_hash_list(buggy_norm_lines)
#                 print('\nHash list\n', hash_list, '\n')
                self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_buggy_lines), buggy_norm_lines, hash_list))
            if removed_lines:
                removed_norm_lines = []
                for removed in removed_lines:
                    removed_norm_lines.append(self._normalize(''.join(removed), magic_ext).split())
#                     hash1_r = common.fnv1a_hash(ngram) & (common.bloomfilter_size-1)
#                     hash2_r = common.djb2_hash(ngram) & (common.bloomfilter_size-1)
#                     hash3_r = common.sdbm_hash(ngram) & (common.bloomfilter_size-1)
#                     hash_list_removed = [hash1_r, hash2_r, hash3_r]
                    self._only_removed.append(removed_norm_lines)
                    
    def _process_patch(self, patch_path):
        '''
        Normalize a patch file and build a hash list
        '''
        patch_filename = patch_path.split('/')[-1]
        patch_file = open(patch_path, 'r')
        patch_lines = patch_file.readlines()
        patch_file.close()
        
        magic_ext = None
        process_flag = False
        diff_file = ''
        diff_cnt = 0
        diff_patch_lines = []
        orig_norm_lines = []
        diff_orig_lines = []
        
        added_lines = []
        
        for line in patch_lines:
            diff_file = re.sub('\.patch$', '', patch_path)
            magic_ext = self._get_file_type(diff_file)
            if line.startswith('@@'):
                if diff_patch_lines:
#                     common.verbose_print('\nDiff patch lines')
#                     common.verbose_print(diff_patch_lines)
                    diff_norm_lines = self._normalize(''.join(diff_patch_lines), magic_ext).split()
#                     common.verbose_print('\nDiff norm lines')
#                     common.verbose_print(diff_norm_lines)
                    if len(diff_norm_lines) >= common.ngram_size:
                        common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                        path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                        hash_list = self._build_hash_list(diff_norm_lines)
#                         common.verbose_print('hash list')
#                         common.verbose_print(hash_list)
                        self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_orig_lines), diff_norm_lines, hash_list))
                    else:
#                         common.verbose_print('Adjusting ngram_size')
                        common.ngram_size = len(diff_norm_lines)
#                         common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                        path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                        hash_list = self._build_hash_list(diff_norm_lines)
#                         common.verbose_print('hash list')
#                         common.verbose_print(hash_list)
                        self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_orig_lines), diff_norm_lines, hash_list))
                    del diff_patch_lines[:]                   
                    del orig_norm_lines[:]
                if added_lines:
                    added_norm_lines = []
                    for added in added_lines:
                        added_norm_lines.append(self._normalize(''.join(added), magic_ext).split())
#                         hash1_a = common.fnv1a_hash(ngram) & (common.bloomfilter_size-1)
#                         hash2_a = common.djb2_hash(ngram) & (common.bloomfilter_size-1)
#                         hash3_a = common.sdbm_hash(ngram) & (common.bloomfilter_size-1)
#                         hash_list_added = [hash1_a, hash2_a, hash3_a]
                        self._only_added.append(added_norm_lines)
                    del added_lines[:]
                    
                diff_cnt += 1

            elif line.startswith('+'):
                diff_patch_lines.append(line[1:])
                diff_orig_lines.append('<font color=\"#00AA00\">')
                diff_orig_lines.append(line.replace('<','&lt;').replace('>','&gt;'))
                diff_orig_lines.append('</font>')
                added_lines.append(line[1:])
                
            elif line.startswith(' '):
                diff_patch_lines.append(line[1:])
                diff_orig_lines.append(line.replace('<','&lt;').replace('>','&gt;'))

#         print('\nDiff patch lines')
#         print(diff_patch_lines)
        if diff_patch_lines:
            diff_norm_lines = self._normalize(''.join(diff_patch_lines), magic_ext).split()
#             common.verbose_print('\nDiff norm lines')
#             common.verbose_print(diff_norm_lines)
            if len(diff_norm_lines) >= common.ngram_size:
#                 common.verbose_print('      %s %d (ext: %d)' % (diff_file, diff_cnt, magic_ext))
                path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                hash_list = self._build_hash_list(diff_norm_lines)
#                 common.verbose_print('\nHash list\n', hash_list, '\n')
                self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_patch_lines), diff_norm_lines, hash_list))
            else:
#                 common.verbose_print('Adjusting ngram_size')
#                 common.ngram_size = len(diff_norm_lines)
                path = '[%s] %s #%d' % (patch_filename, diff_file, diff_cnt)
                hash_list = self._build_hash_list(diff_norm_lines)
#                 common.verbose_print('\nHash list\n')
#                 common.verbose_print(hash_list)
                self._patch_list.append(common.PatchInfo(path, magic_ext, ''.join(diff_patch_lines), diff_norm_lines, hash_list))
            if added_lines:
                added_norm_lines = []
                for added in added_lines:
                    added_norm_lines.append(self._normalize(''.join(added), magic_ext).split())
                    self._only_added.append(added_norm_lines)
#                     hash1_a = common.fnv1a_hash(added) & (common.bloomfilter_size-1)
#                     hash2_a = common.djb2_hash(added) & (common.bloomfilter_size-1)
#                     hash3_a = common.sdbm_hash(added) & (common.bloomfilter_size-1)
#                     hash_list_added = [hash1_a, hash2_a, hash3_a]

    def _normalize(self, patch, ext):
        '''
        Normalize a patch file
        '''
        # Language-specific optimization
        if ext==common.FileExt.C or ext==common.FileExt.Java:
            patch = ''.join([c.group('noncomment') for c in common.c_regex.finditer(patch) if c.group('noncomment')])
            patch = ''.join([c.group('noncomment') for c in common.c_partial_comment_regex.finditer(patch) if c.group('noncomment')])
        elif ext==common.FileExt.ShellScript:
            patch = ''.join([c.group('noncomment') for c in common.shellscript_regex.finditer(patch) if c.group('noncomment')])
        elif ext==common.FileExt.Python:
            patch = re.sub(re.compile("'''.*?'''", re.DOTALL ), "", patch) # Remove multi-line comments with single quotes
            patch = re.sub(re.compile('""".*?"""', re.DOTALL ), "", patch) # Remove multi-line comments with double quotes
            patch = re.sub(re.compile("#.*?\n"), "", patch) # Remove single line comments
        elif ext==common.FileExt.Perl:
            patch = ''.join([c.group('noncomment') for c in common.perl_regex.finditer(patch) if c.group('noncomment')])
        elif ext==common.FileExt.PHP:
            patch = ''.join([c.group('noncomment') for c in common.php_regex.finditer(patch) if c.group('noncomment')])
            patch = ''.join([c.group('noncomment') for c in common.c_partial_comment_regex.finditer(patch) if c.group('noncomment')])
        elif ext==common.FileExt.Ruby:
            patch = ''.join([c.group('noncomment') for c in common.ruby_regex.finditer(patch) if c.group('noncomment')])
            patch = ''.join([c.group('noncomment') for c in common.ruby_partial_comment_regex.finditer(patch) if c.group('noncomment')])

        # Remove whitespaces except newlines
        patch = common.whitespaces_regex.sub("", patch)
        # Convert into lowercases
        return patch.lower()

    def _build_hash_list(self, diff_norm_lines):
        '''
        Build a hash list
        '''
        hash_list = []
        num_ngram = len(diff_norm_lines) - common.ngram_size + 1
        
        for i in range(0, num_ngram):
            ngram = ''.join(diff_norm_lines[i:i+common.ngram_size])
            hash1 = common.fnv1a_hash(ngram) & (common.bloomfilter_size-1)
            hash2 = common.djb2_hash(ngram) & (common.bloomfilter_size-1)
            hash3 = common.sdbm_hash(ngram) & (common.bloomfilter_size-1)
            hash_list.append(hash1)
            hash_list.append(hash2)
            hash_list.append(hash3)
            
            self._hashes[hash1] = ngram
            self._hashes[hash2] = ngram
            self._hashes[hash3] = ngram
        return hash_list

    def _get_file_type(self, file_path):
        '''
        Guess a file type based upon a file extension (mimetypes module)
        '''
        file_type, encoding = mimetypes.guess_type(file_path)
        magic_ext = None
        if file_type is None:
            magic_ext = common.FileExt.Text
        else:
            main_type, sub_type = file_type.split('/')
            if sub_type.startswith('x-c'):
                magic_ext = common.FileExt.C
            elif sub_type == 'x-java':
                magic_ext = common.FileExt.Java
            elif sub_type == 'x-sh':
                magic_ext = common.FileExt.ShellScript
            elif sub_type == 'x-perl':
                magic_ext = common.FileExt.Perl
            elif sub_type == 'x-python':
                magic_ext = common.FileExt.Python
            elif sub_type == 'x-httpd-php':
                magic_ext = common.FileExt.PHP
            elif sub_type == 'x-ruby':
                magic_ext = common.FileExt.Ruby
            else:
                magic_ext = common.FileExt.Text
        return magic_ext

    def items(self):
        return self._patch_list

    def length(self):
        return self._npatch
    
    def hashes(self):
        return self._hashes

    def added(self):
        return self._only_added
    
    def removed(self):
        return self._only_removed